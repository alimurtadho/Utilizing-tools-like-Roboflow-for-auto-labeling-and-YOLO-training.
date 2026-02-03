"""
YOLOv8 Helmet Detection Model
Object detection for motorcycles and helmets
"""

import logging
import cv2
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from ultralytics import YOLO
from models.helmet_analyzer import HelmetAnalyzer

logger = logging.getLogger(__name__)

class HelmetDetector:
    """YOLOv8 based helmet detection"""
    
    def __init__(self, model_size: str = "n", device: str = "auto"):
        """
        Initialize detector
        
        Args:
            model_size: n (nano), s (small), m (medium), l (large), x (xlarge)
            device: auto, cpu, cuda, mps
        """
        self.model_size = model_size
        self.device = self._get_device(device)
        self.model = self._load_model()
        self.helmet_analyzer = HelmetAnalyzer()  # Advanced helmet detection
        
        # COCO class IDs (YOLOv8 default)
        self.class_names = {
            0: "person",
            1: "bicycle",
            2: "car",
            3: "motorcycle",
            4: "bus"
        }
        
        logger.info(f"✅ HelmetDetector initialized on {self.device}")
    
    def _get_device(self, device: str) -> str:
        """Get appropriate device"""
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            # MPS has issues with NMS operation - use CPU for stability
            # elif torch.backends.mps.is_available():
            #     return "mps"
            else:
                return "cpu"
        return device
    
    def _load_model(self) -> YOLO:
        """Load YOLOv8 model"""
        try:
            logger.info(f"Loading YOLOv8{self.model_size}...")
            model = YOLO(f"yolov8{self.model_size}.pt")
            model.to(self.device)
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def detect(self, frame: np.ndarray, confidence: float = 0.25) -> Dict:
        """
        Run detection on single frame
        
        Args:
            frame: Input image (BGR)
            confidence: Confidence threshold
            
        Returns:
            Detection results
        """
        try:
            # Run inference
            results = self.model(frame, conf=confidence, verbose=False)
            
            detections = {
                "motorcycles": [],
                "people": [],
                "helmets": [],
                "boxes": []
            }
            
            if results[0].boxes is not None:
                for box in results[0].boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    bbox = box.xyxy[0].cpu().numpy()
                    
                    detection = {
                        "class": cls,
                        "class_name": self.class_names.get(cls, "unknown"),
                        "confidence": conf,
                        "box": bbox.tolist()  # [x1, y1, x2, y2]
                    }
                    
                    if cls == 3:  # motorcycle (COCO ID)
                        detections["motorcycles"].append(detection)
                    elif cls == 0:  # person (COCO ID)
                        detections["people"].append(detection)
                    # Note: Standard YOLOv8 doesn't have helmet classes
                    # Helmet detection done via head region analysis
                    
                    detections["boxes"].append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return {"motorcycles": [], "people": [], "helmets": [], "boxes": []}
    
    def process_video(
        self,
        video_path: str,
        roi: Optional[List[List[int]]] = None,
        confidence: float = 0.25,  # Lower threshold for CCTV
        skip_frames: int = 1,
        max_frames: Optional[int] = None
    ) -> Dict:
        """
        Process entire video
        
        Args:
            video_path: Path to video file
            roi: Region of Interest polygon [[x1,y1], [x2,y2], ...]
            confidence: Detection confidence threshold
            skip_frames: Process every nth frame
            max_frames: Maximum frames to process (for testing)
            
        Returns:
            Processing results with detections and statistics
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            logger.info(f"Video: {width}x{height} @ {fps}fps, {total_frames} frames")
            
            # Convert ROI to polygon mask if provided
            roi_mask = None
            if roi:
                roi_mask = self._create_roi_mask(roi, width, height)
            
            # Results storage
            detections = []
            motorcycle_ids = set()
            helmets_count = 0
            no_helmets_count = 0
            frame_count = 0
            processed_count = 0
            
            # Process frames
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Skip frames
                if frame_count % skip_frames != 0:
                    continue
                
                # Apply ROI mask if provided
                if roi_mask is not None:
                    frame_masked = cv2.bitwise_and(frame, frame, mask=roi_mask)
                else:
                    frame_masked = frame
                
                # Run detection
                detection_result = self.detect(frame_masked, confidence)
                
                # Match people to motorcycles and analyze helmets
                matches = self.helmet_analyzer.match_people_to_motorcycles(
                    detection_result["people"],
                    detection_result["motorcycles"]
                )
                
                # Analyze helmet for each person on motorcycle
                helmet_results = []
                for person, motorcycle in matches:
                    helmet_analysis = self.helmet_analyzer.analyze_person_on_motorcycle(
                        frame_masked,
                        person['box'],
                        motorcycle['box']
                    )
                    helmet_results.append(helmet_analysis)
                
                # Process detections
                frame_data = {
                    "frame_number": frame_count,
                    "timestamp": frame_count / fps if fps > 0 else 0,
                    "motorcycles": len(detection_result["motorcycles"]),
                    "occupants": len(matches),  # Only count people on motorcycles
                    "helmets": sum(1 for h in helmet_results if h.get('has_helmet')),
                    "no_helmets": sum(1 for h in helmet_results if not h.get('has_helmet')),
                    "detections": detection_result["boxes"],
                    "helmet_analysis": helmet_results
                }
                
                # Count helmet status
                helmets_count += frame_data["helmets"]
                no_helmets_count += frame_data["no_helmets"]
                
                # Track motorcycles
                for moto in detection_result["motorcycles"]:
                    moto_id = f"moto_{frame_count}_{len(motorcycle_ids)}"
                    motorcycle_ids.add(moto_id)
                
                detections.append(frame_data)
                processed_count += 1
                
                # Limit for testing
                if max_frames and processed_count >= max_frames:
                    break
            
            cap.release()
            
            # Calculate statistics
            total_helmets = helmets_count + no_helmets_count
            compliance_rate = (helmets_count / total_helmets * 100) if total_helmets > 0 else 0
            
            results = {
                "total_frames": total_frames,
                "processed_frames": processed_count,
                "motorcycles_detected": len(motorcycle_ids),
                "total_occupants": sum(d["occupants"] for d in detections),
                "helmets_worn": helmets_count,
                "helmets_not_worn": no_helmets_count,
                "compliance_rate": round(compliance_rate, 2),
                "video_duration_seconds": total_frames / fps if fps > 0 else 0,
                "detections": detections,
                "summary": {
                    "motorcycles": len(motorcycle_ids),
                    "compliance_percentage": compliance_rate,
                    "processed_frames": processed_count,
                    "average_occupants_per_frame": round(
                        sum(d["occupants"] for d in detections) / processed_count,
                        2
                    ) if processed_count > 0 else 0
                }
            }
            
            logger.info(f"✅ Video processing complete: {processed_count} frames, "
                       f"{len(motorcycle_ids)} motorcycles, "
                       f"{compliance_rate:.1f}% compliance")
            
            return results
            
        except Exception as e:
            logger.error(f"Video processing error: {e}")
            raise
    
    def _create_roi_mask(self, roi: List[List[int]], width: int, height: int) -> np.ndarray:
        """Create mask for ROI"""
        mask = np.zeros((height, width), dtype=np.uint8)
        points = np.array(roi, dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)
        return mask
    
    def draw_detections(
        self,
        frame: np.ndarray,
        detections: Dict
    ) -> np.ndarray:
        """Draw detection boxes on frame"""
        frame_copy = frame.copy()
        
        # Draw motorcycles (green)
        for moto in detections["motorcycles"]:
            box = moto["box"]
            cv2.rectangle(frame_copy, (int(box[0]), int(box[1])), 
                         (int(box[2]), int(box[3])), (0, 255, 0), 2)
            cv2.putText(frame_copy, f"Motorcycle {moto['confidence']:.2f}",
                       (int(box[0]), int(box[1]) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw people (blue)
        for person in detections["people"]:
            box = person["box"]
            cv2.rectangle(frame_copy, (int(box[0]), int(box[1])), 
                         (int(box[2]), int(box[3])), (255, 0, 0), 2)
        
        # Draw helmets (green for helmet, red for no-helmet)
        for helmet in detections["helmets"]:
            box = helmet["box"]
            color = (0, 255, 0) if helmet["class"] == 2 else (0, 0, 255)
            label = "Helmet" if helmet["class"] == 2 else "No Helmet"
            cv2.rectangle(frame_copy, (int(box[0]), int(box[1])), 
                         (int(box[2]), int(box[3])), color, 2)
            cv2.putText(frame_copy, label, (int(box[0]), int(box[1]) - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return frame_copy

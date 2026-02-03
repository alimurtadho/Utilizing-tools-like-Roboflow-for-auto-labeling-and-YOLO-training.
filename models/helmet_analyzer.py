"""
Advanced Helmet Detection Analyzer
Uses head region analysis and color/shape features
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class HelmetAnalyzer:
    """Analyze helmet presence using computer vision techniques"""
    
    def __init__(self):
        """Initialize helmet analyzer"""
        # Helmet color ranges in HSV
        self.helmet_colors = {
            'red': [(0, 100, 100), (10, 255, 255)],
            'red2': [(170, 100, 100), (180, 255, 255)],
            'blue': [(100, 100, 100), (130, 255, 255)],
            'white': [(0, 0, 200), (180, 30, 255)],
            'black': [(0, 0, 0), (180, 255, 50)],
            'yellow': [(20, 100, 100), (30, 255, 255)],
            'green': [(40, 100, 100), (80, 255, 255)]
        }
        
        logger.info("✅ HelmetAnalyzer initialized")
    
    def analyze_person_on_motorcycle(
        self,
        frame: np.ndarray,
        person_box: List[float],
        motorcycle_box: List[float]
    ) -> Dict:
        """
        Analyze if person on motorcycle is wearing helmet
        
        Args:
            frame: Video frame (BGR)
            person_box: [x1, y1, x2, y2] of person
            motorcycle_box: [x1, y1, x2, y2] of motorcycle
            
        Returns:
            Analysis results with helmet status
        """
        try:
            # Get head region (top 25% of person bounding box)
            px1, py1, px2, py2 = [int(x) for x in person_box]
            head_height = int((py2 - py1) * 0.25)
            head_region = frame[py1:py1+head_height, px1:px2]
            
            if head_region.size == 0:
                return {'has_helmet': False, 'confidence': 0.0, 'reason': 'invalid_region'}
            
            # Analyze head region
            helmet_score = self._detect_helmet_in_region(head_region)
            
            result = {
                'has_helmet': helmet_score > 0.35,  # Lowered threshold for CCTV (was 0.5)
                'confidence': float(helmet_score),
                'helmet_color': self._detect_dominant_color(head_region),
                'head_box': [px1, py1, px2, py1+head_height]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Helmet analysis error: {e}")
            return {'has_helmet': False, 'confidence': 0.0, 'reason': 'error'}
    
    def _detect_helmet_in_region(self, head_region: np.ndarray) -> float:
        """
        Detect helmet presence in head region
        
        Args:
            head_region: Cropped head image
            
        Returns:
            Confidence score (0-1)
        """
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(head_region, cv2.COLOR_BGR2HSV)
            
            # Check for helmet-typical colors
            helmet_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
            
            for color_name, (lower, upper) in self.helmet_colors.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                helmet_mask = cv2.bitwise_or(helmet_mask, mask)
            
            # Calculate helmet presence score
            helmet_pixels = np.count_nonzero(helmet_mask)
            total_pixels = head_region.shape[0] * head_region.shape[1]
            
            if total_pixels == 0:
                return 0.0
            
            # Score based on helmet-colored pixels coverage
            coverage = helmet_pixels / total_pixels
            
            # Additional checks
            score = coverage
            
            # Lower threshold for CCTV footage (often low quality)
            # If significant helmet color detected, it's likely a helmet
            if coverage > 0.15:  # Lowered from 0.2 for better detection
                contours, _ = cv2.findContours(helmet_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    area = cv2.contourArea(largest_contour)
                    perimeter = cv2.arcLength(largest_contour, True)
                    
                    if perimeter > 0:
                        circularity = 4 * np.pi * area / (perimeter * perimeter)
                        # Boost score if shape is round-ish (helmet characteristic)
                        score = (coverage * 0.6) + (circularity * 0.4)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Helmet detection error: {e}")
            return 0.0
    
    def _detect_dominant_color(self, region: np.ndarray) -> str:
        """Detect dominant color in region"""
        try:
            hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
            
            # Check each color
            max_pixels = 0
            dominant_color = "unknown"
            
            for color_name, (lower, upper) in self.helmet_colors.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                pixels = np.count_nonzero(mask)
                
                if pixels > max_pixels:
                    max_pixels = pixels
                    dominant_color = color_name.replace('2', '')
            
            return dominant_color
            
        except Exception as e:
            return "unknown"
    
    def match_people_to_motorcycles(
        self,
        people: List[Dict],
        motorcycles: List[Dict]
    ) -> List[Tuple[Dict, Dict]]:
        """
        Match detected people to motorcycles based on spatial proximity
        
        Args:
            people: List of person detections with boxes
            motorcycles: List of motorcycle detections with boxes
            
        Returns:
            List of (person, motorcycle) pairs
        """
        matches = []
        
        for person in people:
            p_box = person['box']
            p_center = self._get_center(p_box)
            
            # Find closest motorcycle
            min_distance = float('inf')
            closest_motorcycle = None
            
            for motorcycle in motorcycles:
                m_box = motorcycle['box']
                m_center = self._get_center(m_box)
                
                # Calculate distance
                distance = np.sqrt(
                    (p_center[0] - m_center[0])**2 + 
                    (p_center[1] - m_center[1])**2
                )
                
                # Check if person is above motorcycle (typical riding position)
                if p_center[1] < m_center[1] + 50:  # Person center should be above or near motorcycle
                    # Check IoU overlap
                    iou = self._calculate_iou(p_box, m_box)
                    
                    # Person should have some overlap or be very close
                    if iou > 0.1 or distance < 100:
                        if distance < min_distance:
                            min_distance = distance
                            closest_motorcycle = motorcycle
            
            if closest_motorcycle is not None:
                matches.append((person, closest_motorcycle))
        
        return matches
    
    def _get_center(self, box: List[float]) -> Tuple[float, float]:
        """Get center point of bounding box"""
        x1, y1, x2, y2 = box
        return ((x1 + x2) / 2, (y1 + y2) / 2)
    
    def _calculate_iou(self, box1: List[float], box2: List[float]) -> float:
        """Calculate Intersection over Union"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        # Intersection area
        x_left = max(x1_1, x1_2)
        y_top = max(y1_1, y1_2)
        x_right = min(x2_1, x2_2)
        y_bottom = min(y2_1, y2_2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection = (x_right - x_left) * (y_bottom - y_top)
        
        # Union area
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union = box1_area + box2_area - intersection
        
        return intersection / union if union > 0 else 0.0

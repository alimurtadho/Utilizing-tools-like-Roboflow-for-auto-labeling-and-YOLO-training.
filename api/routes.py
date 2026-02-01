"""
API Routes - FastAPI endpoints
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import os
import uuid
from datetime import datetime

from api.schemas import (
    VideoUploadResponse,
    VideoListResponse,
    ProcessRequest,
    ResultsResponse,
    AnalyticsResponse
)
from config.settings import settings
from models.detector import HelmetDetector

logger = logging.getLogger(__name__)
router = APIRouter(tags=["API"])

# In-memory storage (replace with database in production)
videos_db = {}
results_db = {}

# Initialize detector
detector = None

def get_detector():
    """Lazy load detector"""
    global detector
    if detector is None:
        logger.info("Initializing YOLOv8 detector...")
        detector = HelmetDetector(model_size=settings.YOLO_MODEL_SIZE)
    return detector

# ==================== VIDEO ENDPOINTS ====================

@router.post("/videos/upload", response_model=VideoUploadResponse, tags=["Videos"])
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file for processing
    
    - **file**: MP4, AVI, MOV video file (max 100MB)
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file size
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)
        
        if file_size_mb > settings.MAX_VIDEO_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max: {settings.MAX_VIDEO_SIZE_MB}MB"
            )
        
        # Check file extension
        ext = file.filename.split('.')[-1].lower()
        if ext not in settings.ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid format. Allowed: {settings.ALLOWED_FORMATS}"
            )
        
        # Generate ID and save
        video_id = str(uuid.uuid4())
        video_path = os.path.join(settings.STORAGE_PATH, "videos", f"{video_id}.{ext}")
        
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        
        with open(video_path, "wb") as f:
            f.write(contents)
        
        # Store metadata
        videos_db[video_id] = {
            "id": video_id,
            "filename": file.filename,
            "file_size_mb": file_size_mb,
            "uploaded_at": datetime.now().isoformat(),
            "status": "pending",
            "path": video_path,
            "format": ext
        }
        
        logger.info(f"Video uploaded: {video_id} ({file_size_mb:.2f}MB)")
        
        return {
            "video_id": video_id,
            "filename": file.filename,
            "size_mb": file_size_mb,
            "status": "pending",
            "message": "Video uploaded successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos", response_model=VideoListResponse, tags=["Videos"])
async def list_videos(skip: int = 0, limit: int = 20):
    """List all uploaded videos"""
    try:
        videos = list(videos_db.values())
        total = len(videos)
        items = videos[skip:skip + limit]
        
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": items
        }
    except Exception as e:
        logger.error(f"List videos error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/videos/{video_id}", tags=["Videos"])
async def get_video(video_id: str):
    """Get video metadata"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return videos_db[video_id]

@router.delete("/videos/{video_id}", tags=["Videos"])
async def delete_video(video_id: str):
    """Delete a video"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        video_path = videos_db[video_id]["path"]
        if os.path.exists(video_path):
            os.remove(video_path)
        
        del videos_db[video_id]
        if video_id in results_db:
            del results_db[video_id]
        
        logger.info(f"Video deleted: {video_id}")
        return {"message": "Video deleted successfully"}
        
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== PROCESSING ENDPOINTS ====================

@router.post("/videos/{video_id}/process", tags=["Processing"])
async def process_video(
    video_id: str,
    request: ProcessRequest,
    background_tasks: BackgroundTasks
):
    """
    Start processing a video
    
    - **video_id**: ID of uploaded video
    - **roi**: Region of Interest (optional) - [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    """
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        # Update status
        videos_db[video_id]["status"] = "processing"
        videos_db[video_id]["started_at"] = datetime.now().isoformat()
        
        # Queue background task
        background_tasks.add_task(
            _process_video_task,
            video_id,
            request.roi
        )
        
        logger.info(f"Processing started: {video_id}")
        
        return {
            "video_id": video_id,
            "status": "processing",
            "message": "Video processing started",
            "eta_seconds": 300
        }
        
    except Exception as e:
        logger.error(f"Process error: {e}")
        videos_db[video_id]["status"] = "failed"
        videos_db[video_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

async def _process_video_task(video_id: str, roi: list = None):
    """Background task for video processing"""
    try:
        detector = get_detector()
        video_data = videos_db[video_id]
        video_path = video_data["path"]
        
        logger.info(f"Processing video: {video_path}")
        
        # Run detection
        results = detector.process_video(
            video_path,
            roi=roi,
            confidence=settings.CONFIDENCE_THRESHOLD
        )
        
        # Store results
        results_db[video_id] = {
            "video_id": video_id,
            "processed_at": datetime.now().isoformat(),
            "total_frames": results.get("total_frames", 0),
            "motorcycles_detected": results.get("motorcycles_detected", 0),
            "total_occupants": results.get("total_occupants", 0),
            "helmets_worn": results.get("helmets_worn", 0),
            "compliance_rate": results.get("compliance_rate", 0),
            "detections": results.get("detections", []),
            "summary": results.get("summary", {})
        }
        
        # Update video status
        videos_db[video_id]["status"] = "completed"
        videos_db[video_id]["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"Processing completed: {video_id}")
        
    except Exception as e:
        logger.error(f"Processing error for {video_id}: {e}")
        videos_db[video_id]["status"] = "failed"
        videos_db[video_id]["error"] = str(e)

@router.get("/videos/{video_id}/status", tags=["Processing"])
async def get_processing_status(video_id: str):
    """Get processing status"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {
        "video_id": video_id,
        "status": videos_db[video_id]["status"],
        "uploaded_at": videos_db[video_id].get("uploaded_at"),
        "completed_at": videos_db[video_id].get("completed_at"),
        "error": videos_db[video_id].get("error")
    }

# ==================== RESULTS ENDPOINTS ====================

@router.get("/videos/{video_id}/results", response_model=ResultsResponse, tags=["Results"])
async def get_results(video_id: str):
    """Get detection results"""
    if video_id not in videos_db:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video_id not in results_db:
        raise HTTPException(status_code=400, detail="Results not ready. Process video first.")
    
    return results_db[video_id]

@router.get("/videos/{video_id}/export", tags=["Results"])
async def export_results(video_id: str, format: str = "json"):
    """
    Export results in different formats
    
    - **format**: json, csv
    """
    if video_id not in results_db:
        raise HTTPException(status_code=400, detail="Results not ready")
    
    results = results_db[video_id]
    
    if format == "csv":
        # Convert to CSV (simplified)
        csv_content = "timestamp,motorcycle_id,occupants,helmets,compliance\n"
        for detection in results.get("detections", []):
            csv_content += f"{detection.get('timestamp','')},{detection.get('motorcycle_id','')},{detection.get('occupants','')},{detection.get('helmets','')},{detection.get('helmet_worn','')}\n"
        
        return JSONResponse(
            content={"csv": csv_content},
            headers={"Content-Disposition": f"attachment; filename=results_{video_id}.csv"}
        )
    
    else:  # json
        return results

# ==================== ANALYTICS ENDPOINTS ====================

@router.get("/analytics/summary", response_model=AnalyticsResponse, tags=["Analytics"])
async def get_analytics_summary():
    """Get overall analytics summary"""
    if not results_db:
        return {
            "total_videos_processed": 0,
            "total_motorcycles": 0,
            "total_occupants": 0,
            "average_compliance_rate": 0,
            "videos": []
        }
    
    total_motorcycles = sum(r.get("motorcycles_detected", 0) for r in results_db.values())
    total_occupants = sum(r.get("total_occupants", 0) for r in results_db.values())
    avg_compliance = sum(r.get("compliance_rate", 0) for r in results_db.values()) / len(results_db)
    
    return {
        "total_videos_processed": len(results_db),
        "total_motorcycles": total_motorcycles,
        "total_occupants": total_occupants,
        "average_compliance_rate": round(avg_compliance, 2),
        "videos": [
            {
                "video_id": r["video_id"],
                "motorcycles": r.get("motorcycles_detected", 0),
                "compliance_rate": r.get("compliance_rate", 0)
            }
            for r in results_db.values()
        ]
    }

logger.info("✅ API routes initialized")

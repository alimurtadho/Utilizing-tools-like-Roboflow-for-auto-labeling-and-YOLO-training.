"""
Pydantic Schemas - Request/Response Models
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

# ==================== VIDEO SCHEMAS ====================

class VideoUploadResponse(BaseModel):
    """Response for video upload"""
    video_id: str
    filename: str
    size_mb: float
    status: str
    message: str

class VideoMetadata(BaseModel):
    """Video metadata"""
    id: str
    filename: str
    file_size_mb: float
    uploaded_at: str
    status: str
    format: str

class VideoListResponse(BaseModel):
    """Response for video list"""
    total: int
    skip: int
    limit: int
    items: List[VideoMetadata]

# ==================== PROCESSING SCHEMAS ====================

class ProcessRequest(BaseModel):
    """Request for video processing"""
    roi: Optional[List[List[int]]] = None  # Region of Interest polygon
    confidence_threshold: Optional[float] = 0.70
    skip_frames: Optional[int] = 1

class ProcessStatus(BaseModel):
    """Processing status"""
    video_id: str
    status: str  # pending, processing, completed, failed
    progress_percent: Optional[int] = None
    eta_seconds: Optional[int] = None
    error: Optional[str] = None

# ==================== DETECTION SCHEMAS ====================

class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x1: float
    y1: float
    x2: float
    y2: float

class Detection(BaseModel):
    """Single detection result"""
    frame_number: int
    timestamp: float
    motorcycle_id: str
    occupants: int
    helmets_worn: int
    helmet_compliance: bool
    confidence: float
    bounding_boxes: List[BoundingBox]
    line_crossed: Optional[bool] = False

class ResultsResponse(BaseModel):
    """Detection results response"""
    video_id: str
    processed_at: str
    total_frames: int
    motorcycles_detected: int
    total_occupants: int
    helmets_worn: int
    compliance_rate: float
    detections: List[Detection]
    summary: Dict

# ==================== ANALYTICS SCHEMAS ====================

class VideoAnalytics(BaseModel):
    """Video-level analytics"""
    video_id: str
    motorcycles: int
    compliance_rate: float
    processed_at: Optional[str] = None

class AnalyticsResponse(BaseModel):
    """Overall analytics response"""
    total_videos_processed: int
    total_motorcycles: int
    total_occupants: int
    average_compliance_rate: float
    videos: List[VideoAnalytics]

# ==================== ERROR SCHEMAS ====================

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: str
    status_code: int
    timestamp: str

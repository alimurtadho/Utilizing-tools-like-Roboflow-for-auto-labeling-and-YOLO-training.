"""Application Constants"""

# Detection Classes
DETECTION_CLASSES = {
    0: "motorcycle",
    1: "person",
    2: "helmet",
    3: "no-helmet"
}

# Status Codes
STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# Video Formats
ALLOWED_FORMATS = {"mp4", "avi", "mov", "mkv", "flv", "wmv"}

# Confidence Thresholds
MIN_HELMET_CONFIDENCE = 0.70
MIN_MOTORCYCLE_CONFIDENCE = 0.60
MIN_PERSON_CONFIDENCE = 0.65

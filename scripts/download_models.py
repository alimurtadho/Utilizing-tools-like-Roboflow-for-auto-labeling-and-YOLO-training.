"""
Download YOLOv8 Models
"""

import logging
import os
from pathlib import Path
from ultralytics import YOLO

logger = logging.getLogger(__name__)

def download_models():
    """Download YOLOv8 models"""
    
    try:
        model_path = Path("models/weights")
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Model sizes to download
        models = {
            "yolov8n": "Nano (fastest, least accurate)",
            "yolov8s": "Small (balanced)",
            "yolov8m": "Medium (default)",
        }
        
        logger.info("📥 Downloading YOLOv8 models...")
        
        for model_name, description in models.items():
            print(f"\n⏳ Downloading {model_name} - {description}")
            
            # Download model (saves to ~/.yolov8/runs/)
            model = YOLO(f"{model_name}.pt")
            
            logger.info(f"✅ {model_name} ready")
        
        logger.info("\n✅ All models downloaded successfully!")
        logger.info(f"📁 Models stored in: {model_path.absolute()}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Download error: {e}")
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_models()

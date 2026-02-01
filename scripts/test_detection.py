"""
Test Detection on Sample Video
"""

import logging
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.detector import HelmetDetector
import json

logger = logging.getLogger(__name__)

def test_detection(video_path: str, roi: list = None):
    """Test detection on a video"""
    
    try:
        if not Path(video_path).exists():
            print(f"❌ Video not found: {video_path}")
            return False
        
        print(f"\n🎥 Testing detection on: {video_path}")
        print("=" * 60)
        
        # Initialize detector
        print("📦 Loading YOLOv8 model...")
        detector = HelmetDetector(model_size="n")  # Use nano for speed
        
        # Process video
        print("⏳ Processing video...")
        results = detector.process_video(
            video_path,
            roi=roi,
            confidence=0.70,
            skip_frames=5,
            max_frames=100  # Limit for testing
        )
        
        # Print results
        print("\n✅ DETECTION RESULTS")
        print("=" * 60)
        print(f"Processed Frames: {results['processed_frames']}")
        print(f"Motorcycles Detected: {results['motorcycles_detected']}")
        print(f"Total Occupants: {results['total_occupants']}")
        print(f"Helmets Worn: {results['helmets_worn']}")
        print(f"No Helmets: {results['helmets_not_worn']}")
        print(f"Compliance Rate: {results['compliance_rate']}%")
        print(f"Video Duration: {results['video_duration_seconds']:.2f}s")
        
        # Sample detections
        if results['detections']:
            print("\n📊 Sample Detections (first 5 frames):")
            print("-" * 60)
            for detection in results['detections'][:5]:
                print(f"Frame {detection['frame_number']}: "
                      f"{detection['motorcycles']} motorcycles, "
                      f"{detection['occupants']} occupants, "
                      f"{detection['helmets']} helmets")
        
        # Save summary
        output_file = Path(video_path).stem + "_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test helmet detection")
    parser.add_argument("--video", required=True, help="Video file path")
    parser.add_argument("--roi", type=str, help="ROI as JSON string")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    roi = None
    if args.roi:
        try:
            import json
            roi = json.loads(args.roi)
        except:
            print("Invalid ROI JSON")
    
    success = test_detection(args.video, roi)
    sys.exit(0 if success else 1)

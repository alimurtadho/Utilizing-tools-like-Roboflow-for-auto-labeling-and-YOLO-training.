"""
Line Crossing Detection Algorithm
For unique motorcycle counting
"""

import logging
import numpy as np
from typing import List, Tuple, Dict, Set

logger = logging.getLogger(__name__)

class LineCrossingDetector:
    """Detects and counts line crossings"""
    
    def __init__(self, line_start: Tuple[int, int], line_end: Tuple[int, int]):
        """
        Initialize detector
        
        Args:
            line_start: (x1, y1) - Start point of counting line
            line_end: (x2, y2) - End point of counting line
        """
        self.line_start = np.array(line_start, dtype=np.float32)
        self.line_end = np.array(line_end, dtype=np.float32)
        self.crossed_ids: Set[str] = set()
        self.crossings: List[Dict] = []
        
        logger.info(f"Line crossing detector initialized")
    
    def point_to_line_distance(self, point: np.ndarray) -> float:
        """Calculate perpendicular distance from point to line"""
        line_vec = self.line_end - self.line_start
        point_vec = point - self.line_start
        line_len = np.linalg.norm(line_vec)
        
        if line_len == 0:
            return np.linalg.norm(point_vec)
        
        line_unitvec = line_vec / line_len
        point_vec_scaled = point_vec / line_len
        t = np.dot(line_unitvec, point_vec_scaled)
        
        if t < 0.0:
            return np.linalg.norm(point_vec)
        elif t > 1.0:
            return np.linalg.norm(point_vec - line_vec)
        else:
            nearest = line_unitvec * t
            return np.linalg.norm(point_vec - nearest)
    
    def segments_intersect(
        self,
        p1: np.ndarray,
        p2: np.ndarray
    ) -> bool:
        """Check if line segment p1-p2 intersects with counting line"""
        
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        A = self.line_start
        B = self.line_end
        C = p1
        D = p2
        
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
    
    def check_crossing(
        self,
        track_id: str,
        prev_center: Tuple[float, float],
        curr_center: Tuple[float, float],
        frame_number: int
    ) -> bool:
        """
        Check if track crossed the line
        
        Args:
            track_id: Unique identifier for tracked object
            prev_center: Previous frame center point
            curr_center: Current frame center point
            frame_number: Current frame number
            
        Returns:
            True if unique crossing detected
        """
        prev_pos = np.array(prev_center, dtype=np.float32)
        curr_pos = np.array(curr_center, dtype=np.float32)
        
        # Check if path intersects counting line
        if self.segments_intersect(prev_pos, curr_pos):
            
            # Check if already counted
            if track_id not in self.crossed_ids:
                self.crossed_ids.add(track_id)
                
                # Log crossing
                crossing = {
                    "track_id": track_id,
                    "frame": frame_number,
                    "position": curr_center,
                    "direction": self._get_direction(prev_pos, curr_pos)
                }
                self.crossings.append(crossing)
                
                logger.debug(f"Crossing detected: {track_id} at frame {frame_number}")
                return True
        
        return False
    
    def _get_direction(self, p1: np.ndarray, p2: np.ndarray) -> str:
        """Determine direction of movement"""
        delta = p2 - p1
        angle = np.arctan2(delta[1], delta[0])
        
        # Relative to line direction
        line_vec = self.line_end - self.line_start
        line_angle = np.arctan2(line_vec[1], line_vec[0])
        
        relative_angle = angle - line_angle
        
        if -np.pi/2 < relative_angle < np.pi/2:
            return "forward"
        else:
            return "backward"
    
    def get_count(self) -> int:
        """Get total unique crossings"""
        return len(self.crossed_ids)
    
    def get_crossings(self) -> List[Dict]:
        """Get all crossing records"""
        return self.crossings
    
    def reset(self):
        """Reset detector"""
        self.crossed_ids.clear()
        self.crossings.clear()
        logger.info("Line crossing detector reset")

# Alternative: Simple vertical line crossing
class VerticalLineCrossing:
    """Simple vertical line crossing detection"""
    
    def __init__(self, x_threshold: int):
        """
        Initialize with vertical line at x position
        
        Args:
            x_threshold: X coordinate of vertical line
        """
        self.x_threshold = x_threshold
        self.crossed_ids: Set[str] = set()
    
    def check_crossing(
        self,
        track_id: str,
        prev_x: float,
        curr_x: float
    ) -> bool:
        """Check if object crossed the vertical line"""
        
        # Crossed from left to right
        if prev_x < self.x_threshold <= curr_x:
            if track_id not in self.crossed_ids:
                self.crossed_ids.add(track_id)
                return True
        
        # Crossed from right to left
        elif prev_x > self.x_threshold >= curr_x:
            if track_id not in self.crossed_ids:
                self.crossed_ids.add(track_id)
                return True
        
        return False
    
    def get_count(self) -> int:
        """Get total crossings"""
        return len(self.crossed_ids)

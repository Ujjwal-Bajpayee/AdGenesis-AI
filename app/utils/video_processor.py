import os
import cv2
import numpy as np
from typing import List, Dict, Any
from app.core.logger import logger

class VideoProcessor:
    def extract_keyframes_and_metadata(self, video_path: str, output_dir: str, max_frames: int = 10) -> Dict[str, Any]:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found at {video_path}")
            
        os.makedirs(output_dir, exist_ok=True)
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            return {
                "duration_seconds": 0.0,
                "fps": 0.0,
                "total_frames": 0,
                "frame_paths": [],
                "scenes_count": 0,
                "pacing": "Unknown",
                "motion_score": 0.0
            }

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        duration_seconds = float(total_frames / fps) if fps > 0 else 0.0
        
        frame_indices = []
        if total_frames > 0:
            step = max(1, total_frames // max_frames)
            frame_indices = [i for i in range(0, total_frames, step)][:max_frames]
            
        frame_paths = []
        prev_frame = None
        motion_diffs = []
        scene_changes = 0

        current_idx = 0
        saved_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_frame is not None:
                diff = cv2.absdiff(gray, prev_frame)
                mean_diff = float(np.mean(diff))
                motion_diffs.append(mean_diff)
                if mean_diff > 35.0:
                    scene_changes += 1
            prev_frame = gray
            
            if current_idx in frame_indices and saved_count < max_frames:
                frame_filename = f"frame_{saved_count:03d}.jpg"
                frame_path = os.path.join(output_dir, frame_filename)
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
                saved_count += 1
                
            current_idx += 1

        cap.release()
        
        avg_motion = float(np.mean(motion_diffs)) if motion_diffs else 0.0
        pacing = "Fast" if avg_motion > 20.0 or scene_changes > 4 else ("Medium" if avg_motion > 10.0 else "Slow")

        return {
            "duration_seconds": round(duration_seconds, 2),
            "fps": round(fps, 2),
            "total_frames": total_frames,
            "frame_paths": frame_paths,
            "scenes_count": max(1, scene_changes + 1),
            "pacing": pacing,
            "motion_score": round(avg_motion, 2)
        }

video_processor = VideoProcessor()

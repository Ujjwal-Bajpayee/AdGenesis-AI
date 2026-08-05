from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class VideoInputSchema(BaseModel):
    video_path: str
    video_filename: str
    duration_seconds: float = 0.0
    frame_paths: List[str] = Field(default_factory=list)

class AudioInputSchema(BaseModel):
    audio_path: str
    duration_seconds: float = 0.0

class OCRInputSchema(BaseModel):
    frame_paths: List[str] = Field(default_factory=list)

class CaptionInputSchema(BaseModel):
    raw_caption: str
    campaign_goal: str

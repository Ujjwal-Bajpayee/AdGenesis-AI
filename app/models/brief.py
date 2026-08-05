from datetime import datetime
from typing import List, Dict, Any
from beanie import Document
from pydantic import Field

class CreativeBriefDocument(Document):
    brief_id: str = Field(index=True, unique=True)
    analysis_id: str = Field(index=True)
    campaign_goal: str
    target_audience: str
    video_duration: str
    opening_hook: str
    scene_by_scene_breakdown: List[Dict[str, Any]] = Field(default_factory=list)
    voiceover_script: str
    music_recommendation: str
    visual_style: str
    cta: str
    caption: str
    hashtags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "creative_briefs"

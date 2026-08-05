from datetime import datetime
from typing import List, Dict, Any, Optional
from beanie import Document
from pydantic import Field

class VideoAnalysisDocument(Document):
    analysis_id: str = Field(index=True, unique=True)
    video_filename: str
    video_path: str
    caption: str
    campaign_goal: str
    status: str = "pending"
    
    video_analysis: Dict[str, Any] = Field(default_factory=dict)
    audio_analysis: Dict[str, Any] = Field(default_factory=dict)
    ocr_analysis: Dict[str, Any] = Field(default_factory=dict)
    caption_analysis: Dict[str, Any] = Field(default_factory=dict)
    creative_synthesis: Dict[str, Any] = Field(default_factory=dict)
    prediction: Dict[str, Any] = Field(default_factory=dict)
    recommendations: Dict[str, Any] = Field(default_factory=dict)
    experiments: List[Dict[str, Any]] = Field(default_factory=list)
    budget_recommendation: Dict[str, Any] = Field(default_factory=dict)
    
    embeddings: List[float] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "video_analyses"

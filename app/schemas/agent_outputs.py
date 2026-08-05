from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class VideoAnalysisOutput(BaseModel):
    key_frames_count: int = 0
    scenes_detected: int = 0
    pacing: str = "Medium"
    products_identified: List[str] = Field(default_factory=list)
    people_detected_count: int = 0
    emotions_detected: List[str] = Field(default_factory=list)
    visual_summary: str = ""
    visual_embedding: List[float] = Field(default_factory=list)

class AudioAnalysisOutput(BaseModel):
    transcript: str = ""
    speaking_speed_wpm: float = 0.0
    emotional_tone: str = "Neutral"
    background_music_mood: str = "Upbeat"
    has_voiceover: bool = False

class OCRAgentOutput(BaseModel):
    raw_texts: List[str] = Field(default_factory=list)
    cleaned_texts: List[str] = Field(default_factory=list)
    detected_ctas: List[str] = Field(default_factory=list)
    text_on_screen_summary: str = ""

class CaptionAnalysisOutput(BaseModel):
    clean_caption: str = ""
    hashtags: List[str] = Field(default_factory=list)
    cta: str = ""
    marketing_intent: str = ""
    semantic_embedding: List[float] = Field(default_factory=list)

class CreativeAnalysisOutput(BaseModel):
    hook_evaluation: str = ""
    storytelling_quality: str = ""
    editing_style: str = ""
    target_audience: str = ""
    brand_messaging: str = ""
    emotional_appeal: str = ""
    product_visibility: str = ""
    visual_consistency: str = ""
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)

class PredictionOutput(BaseModel):
    expected_engagement_rate: str = "0%"
    expected_watch_time_seconds: str = "0s"
    expected_ctr: str = "0%"
    expected_conversions_estimate: str = "0%"
    overall_quality_score: float = 0.0
    reasoning: str = ""

class RecommendationOutput(BaseModel):
    better_hook: str = ""
    better_opening: str = ""
    better_pacing: str = ""
    better_cta: str = ""
    better_caption: str = ""
    better_hashtags: List[str] = Field(default_factory=list)
    better_ending: str = ""
    better_storytelling: str = ""

class CreativeBriefOutput(BaseModel):
    campaign_goal: str = ""
    target_audience: str = ""
    video_duration: str = ""
    opening_hook: str = ""
    scene_by_scene_breakdown: List[Dict[str, Any]] = Field(default_factory=list)
    voiceover_script: str = ""
    music_recommendation: str = ""
    visual_style: str = ""
    cta: str = ""
    caption: str = ""
    hashtags: List[str] = Field(default_factory=list)

class ExperimentIdea(BaseModel):
    title: str = ""
    hypothesis: str = ""
    what_to_change: str = ""
    expected_impact: str = ""
    confidence_score: float = 0.0

class BudgetRecommendationOutput(BaseModel):
    recommended_budget_tier: str = ""
    budget_allocation_percentage: float = 0.0
    justification: str = ""

class MarketingReportOutput(BaseModel):
    creative_summary: str = ""
    predicted_performance: Dict[str, Any] = Field(default_factory=dict)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendations: Dict[str, Any] = Field(default_factory=dict)
    creative_brief: Dict[str, Any] = Field(default_factory=dict)
    budget_recommendation: Dict[str, Any] = Field(default_factory=dict)
    experiments: List[Dict[str, Any]] = Field(default_factory=list)
    full_markdown: str = ""

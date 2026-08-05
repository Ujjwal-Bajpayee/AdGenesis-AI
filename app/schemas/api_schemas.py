from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AnalysisRequestResponse(BaseModel):
    analysis_id: str
    status: str
    message: str

class WorkflowStatusResponse(BaseModel):
    analysis_id: str
    status: str
    current_agent: str
    execution_order: List[str] = Field(default_factory=list)
    agent_logs: List[Dict[str, Any]] = Field(default_factory=list)
    error: Optional[str] = None

class AnalysisDetailResponse(BaseModel):
    analysis_id: str
    video_filename: str
    caption: str
    campaign_goal: str
    status: str
    video_analysis: Dict[str, Any] = Field(default_factory=dict)
    audio_analysis: Dict[str, Any] = Field(default_factory=dict)
    ocr_analysis: Dict[str, Any] = Field(default_factory=dict)
    caption_analysis: Dict[str, Any] = Field(default_factory=dict)
    creative_synthesis: Dict[str, Any] = Field(default_factory=dict)
    prediction: Dict[str, Any] = Field(default_factory=dict)
    recommendations: Dict[str, Any] = Field(default_factory=dict)
    experiments: List[Dict[str, Any]] = Field(default_factory=list)
    budget_recommendation: Dict[str, Any] = Field(default_factory=dict)
    created_at: str

class ExportReportResponse(BaseModel):
    analysis_id: str
    markdown_content: str
    pdf_url: Optional[str] = None

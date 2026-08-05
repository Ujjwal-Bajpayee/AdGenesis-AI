from typing import TypedDict, List, Dict, Any

class AdGenesisState(TypedDict):
    analysis_id: str
    video_path: str
    video_filename: str
    raw_caption: str
    campaign_goal: str
    
    media_metadata: Dict[str, Any]
    raw_ocr_data: Dict[str, Any]
    raw_audio_data: Dict[str, Any]
    
    video_analysis: Dict[str, Any]
    audio_analysis: Dict[str, Any]
    ocr_analysis: Dict[str, Any]
    caption_analysis: Dict[str, Any]
    creative_synthesis: Dict[str, Any]
    prediction: Dict[str, Any]
    recommendations: Dict[str, Any]
    creative_brief: Dict[str, Any]
    experiments: List[Dict[str, Any]]
    budget_recommendation: Dict[str, Any]
    marketing_report: Dict[str, Any]
    
    current_agent: str
    execution_order: List[str]
    agent_logs: List[Dict[str, Any]]
    error: str
    status: str

from datetime import datetime
from typing import Dict, Any, Optional
from beanie import Document
from pydantic import Field

class MarketingReportDocument(Document):
    report_id: str = Field(index=True, unique=True)
    analysis_id: str = Field(index=True)
    title: str
    markdown_content: str
    json_data: Dict[str, Any] = Field(default_factory=dict)
    pdf_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "marketing_reports"

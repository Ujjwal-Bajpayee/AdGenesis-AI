from datetime import datetime
from typing import List, Dict, Any
from beanie import Document
from pydantic import Field

class WorkflowStateDocument(Document):
    workflow_id: str = Field(index=True, unique=True)
    analysis_id: str = Field(index=True)
    current_agent: str
    status: str
    execution_order: List[str] = Field(default_factory=list)
    agent_logs: List[Dict[str, Any]] = Field(default_factory=list)
    error: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "workflow_history"

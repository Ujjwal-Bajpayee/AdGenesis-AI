from abc import ABC, abstractmethod
from typing import Dict, Any
from app.core.llm_factory import get_llm
from app.core.logger import logger

class BaseAgent(ABC):
    def __init__(self, agent_name: str, model_name: str | None = None, temperature: float = 0.2):
        self.agent_name = agent_name
        self.llm = get_llm(model_name=model_name, temperature=temperature)

    @abstractmethod
    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def log_start(self):
        logger.info(f"Agent [{self.agent_name}] execution started.")

    def log_complete(self):
        logger.info(f"Agent [{self.agent_name}] execution completed.")

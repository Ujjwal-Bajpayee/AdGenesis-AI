from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.logger import logger

def get_llm(model_name: str | None = None, temperature: float = 0.2) -> BaseChatModel:
    provider = settings.LLM_PROVIDER.lower()
    target_model = model_name or settings.LLM_MODEL_NAME
    
    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=target_model,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=temperature,
            convert_system_message_to_human=True
        )
    elif provider == "openai":
        return ChatOpenAI(
            model_name=target_model,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE,
            temperature=temperature
        )
    elif provider == "openrouter":
        return ChatOpenAI(
            model_name=target_model,
            api_key=settings.OPENAI_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature
        )
    elif provider == "ollama":
        return ChatOpenAI(
            model_name=target_model,
            api_key="ollama",
            base_url=f"{settings.OLLAMA_BASE_URL.rstrip('/')}/v1",
            temperature=temperature
        )
    else:
        logger.warning(f"Unknown provider '{provider}', defaulting to OpenAI interface")
        return ChatOpenAI(
            model_name=target_model,
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature
        )

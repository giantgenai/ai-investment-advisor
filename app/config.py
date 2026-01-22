from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    openai_chat_model: str = "gpt-4o-mini"
    ollama_chat_model: str = "qwen3-vl:30b"
    ollama_provider: str = "ollama/qwen3-vl:30b"
    ollama_summary_model: str = "qwen2.5:7b"
    ollama_summary_provider: str = "ollama/qwen2.5:7b"
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_api_key: str = "ollama"


MODEL_CONFIG = ModelConfig()

from pathlib import Path

from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


env = Env()
env.read_env()

class Settings(BaseSettings):
    app_name: str = env.str("APP_NAME")
    app_version: str = env.str("APP_VERSION")
    debug: bool = True

    ollama_base_url: str = env.str("OLLAMA_BASE_URL")
    ollama_model: str = env.str("OLLAMA_MODEL")
    embedding_model: str = env.str("EMBEDDING_MODEL")

    chroma_persist_directory: str = env.str("CHROMA_PERSIST_DIRECTORY")
    chroma_collection_name: str = env.str("CHROMA_COLLECTION_NAME")

    retrieval_top_k: int = env.int("RETRIEVAL_TOP_K")
    retrieval_score_threshold: float = env.float("RETRIEVAL_SCORE_THRESHOLD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
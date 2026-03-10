# app/core/config.py
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseSettings):
    # ===============================
    # 应用基础配置
    # ===============================
    APP_NAME: str = Field(default="Orion AI Platform Server", description="项目名称")
    APP_VERSION: str = Field(default="1.0.0")
    APP_DESCRIPTION: str = Field(default="")
    APP_HOST: str = Field(default="127.0.0.1")
    APP_PORT: int = Field(default=8000)
    API_PREFIX: str = Field(default="/v1")
    ENVIRONMENT: str = Field(default="dev")
    LOG_LEVEL: str = Field(default="INFO", description="日志级别: DEBUG, INFO, WARNING, ERROR")
    LOG_DIR: str = Field(default="logs", description="日志存放目录")

    # ===============================
    # PostgreSQL / pgvector
    # ===============================
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # ===============================
    # LLM 配置
    # ===============================
    LLM_PROVIDER: str = Field(default="qwen", description="当前使用的LLM提供商")

    # ===============================
    # LLM / 智谱 配置
    # ===============================
    ZHIPU_API_KEY: str = Field(..., description="Zhipu AI API Key")
    ZHIPU_API_BASE: str = Field(
        default="https://open.bigmodel.cn/api/paas/v4",
        description="Zhipu API base url"
    )
    ZHIPU_MODEL_GLM: str = Field(default="glm-4-flash", description="Chat model")
    ZHIPU_MODEL_EMBEDDING: str = Field(default="embedding-2", description="Embedding model")
    ZHIPU_EMBEDDING_DIM: int = Field(default=4096, description="Embedding vector dimension")

    # ===============================
    # LLM / 千问 配置
    # ===============================
    QWEN_API_KEY: str = Field(..., description="Qwen AI API Key")
    QWEN_API_BASE: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="Qwen API base url"
    )
    QWEN_MODEL_LLM: str = Field(default="qwen-plus", description="Chat model")
    QWEN_MODEL_EMBEDDING: str = Field(default="text-embedding-v3", description="Embedding model")
    QWEN_EMBEDDING_DIM: int = Field(default=1024, description="Embedding vector dimension")

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    # ===============================
    # Settings 行为配置
    # ===============================
    model_config = SettingsConfigDict(
        # 自动向上寻找项目根目录下的 .env 文件
        env_file=os.path.join(ROOT_DIR, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # 忽略多余的环境变量
    )


settings = Settings()

from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    secret_key: str
    debug: bool = False
    log_level: str = "INFO"


class DatabaseSettings(BaseSettings):

    host: str = "localhost"
    port: int = 5432
    postgres_db: str
    user: str
    password: str
    url: str
    url_sync: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        extra="ignore",
    )

    class Config:
        fields = {
            "url": {"env": "DATABASE_URL"},
            "url_sync": {"env": "DATABASE_URL_SYNC"},
            "postgres_db": {"env": 'POSTGRES_DB'}
        }


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=".env", extra="ignore")

    host: str = "localhost"
    port: int = 6379
    password: str = ""
    db: int = 0
    url: str = "redis://localhost:6379/0"


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELERY_", env_file=".env", extra="ignore")

    broker_url: str
    result_backend: str
    task_serializer: str = "json"
    result_serializer: str = "json"
    timezone: str = "UTC"


class AnthropicSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CLAUDE_", env_file=".env", extra="ignore")

    api_key: str
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 4096
    temperature: float = 0.2

    class Config:
        fields = {"api_key": {"env": "ANTHROPIC_API_KEY"}}


class QdrantSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QDRANT_", env_file=".env", extra="ignore")

    host: str = "localhost"
    port: int = 6333
    grpc_port: int = 6334
    api_key: str = ""
    collection_resumes: str = "resumes"
    collection_jobs: str = "jobs"
    vector_size: int = 768

    class Config:
        fields = {"vector_size": {"env": "VECTOR_SIZE"}}


class EmbeddingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EMBEDDING_", env_file=".env", extra="ignore")

    spacy_model: str = "en_core_web_lg"
    model: str = "all-mpnet-base-v2"
    batch_size: int = 32
    device: str = "cpu"

    class Config:
        fields = {"spacy_model": {"env": "SPACY_MODEL"}}


class IngestionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    upload_dir: str = "data/raw"
    processed_dir: str = "data/processed"
    embeddings_dir: str = "data/embeddings"
    jobs_dir: str = "data/jobs"
    max_file_size_mb: int = 10
    allowed_extensions: list[str] = ["pdf", "docx"]

    @field_validator("allowed_extensions", mode="before")
    @classmethod
    def split_extensions(cls, v: str | list) -> list[str]:
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v


class OCRSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OCR_", env_file=".env", extra="ignore")

    tesseract_cmd: str = "tesseract"
    language: str = "eng"
    dpi: int = 300

    class Config:
        fields = {"tesseract_cmd": {"env": "TESSERACT_CMD"}}


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    encryption_key: str
    pii_scrub_enabled: bool = True
    pii_entities: list[str] = [
        "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION", "DATE_TIME"
    ]

    @field_validator("pii_entities", mode="before")
    @classmethod
    def split_entities(cls, v: str | list) -> list[str]:
        if isinstance(v, str):
            return [e.strip() for e in v.split(",")]
        return v


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key_header: str = "X-API-Key"
    api_key: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


class RateLimitSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RATE_LIMIT_", env_file=".env", extra="ignore")

    requests: int = 100
    window_seconds: int = 60


class MLflowSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MLFLOW_", env_file=".env", extra="ignore")

    tracking_uri: str = "http://localhost:5000"
    experiment_name: str = "resume-matching"
    artifact_root: str = "./mlruns"


class ModelTrainingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    model_dir: str = "model/registry/artifacts"
    random_seed: int = 42
    test_size: float = 0.2
    cv_folds: int = 5
    optuna_n_trials: int = 50


class MonitoringSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    prometheus_port: int = 9090
    drift_threshold: float = 0.15
    psi_threshold: float = 0.2
    alert_email: str = "admin@example.com"


class DataRetentionSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    data_retention_days: int = 365
    auto_purge_enabled: bool = False


class FrontendSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    streamlit_port: int = 8501
    api_base_url: str = "http://localhost:8000"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    anthropic: AnthropicSettings = AnthropicSettings()
    qdrant: QdrantSettings = QdrantSettings()
    embedding: EmbeddingSettings = EmbeddingSettings()
    ingestion: IngestionSettings = IngestionSettings()
    ocr: OCRSettings = OCRSettings()
    security: SecuritySettings = SecuritySettings()
    auth: AuthSettings = AuthSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    mlflow: MLflowSettings = MLflowSettings()
    model_training: ModelTrainingSettings = ModelTrainingSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    data_retention: DataRetentionSettings = DataRetentionSettings()
    frontend: FrontendSettings = FrontendSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()

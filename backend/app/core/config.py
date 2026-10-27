from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = REPO_ROOT / "backend"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BACKEND_ROOT / ".env"), extra="ignore", env_prefix="PPE_")

    model_path: str = "../models/ppe_guard_best.pt"
    max_upload_mb: int = Field(default=10, ge=1, le=50)
    max_image_pixels: int = Field(default=16_000_000, ge=100_000, le=100_000_000)
    confidence: float = Field(default=0.25, ge=0.01, le=1)
    iou: float = Field(default=0.45, ge=0.01, le=1)
    image_size: int = Field(default=640, ge=128, le=1536)
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def resolved_model_path(self) -> Path:
        path = Path(self.model_path).expanduser()
        return (path if path.is_absolute() else BACKEND_ROOT / path).resolve()

    @property
    def origins(self) -> list[str]:
        return [s.strip() for s in self.cors_origins.split(",") if s.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

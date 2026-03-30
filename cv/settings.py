import logging
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    root: Path = Path(__file__).resolve().parent.parent

    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    @property
    def build_dir(self) -> Path:
        return self.root / "build"

    @property
    def templates_dir(self) -> Path:
        return self.root / "templates"


def get_settings() -> Settings:
    """Get application settings instance (lazy initialization)."""
    return Settings()


def setup_logging() -> None:
    """Configure logging."""

    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )

    for logger_name in []:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

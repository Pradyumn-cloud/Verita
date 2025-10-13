import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:

    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

    DEFAULT_FRAMEWORK: str = "pytest"
    DEFAULT_OUTPUT_DIR: str = "tests"
    DEFAULT_TEST_PREFIX: str = "test_"

    MIN_COVERAGE: int = 80

    PYTHON_EXTENSIONS: tuple = (".py",)
    EXCLUDE_PATTERNS: tuple = (
        "__pycache__",
        ".pytest_cache",
        ".venv",
        "venv",
        "env",
        ".git",
        "build",
        "dist",
        "*.egg-info",
        "test_*",
        "*_test.py",
    )
    MAX_RETRIES: int = 3
    TIMEOUT: int = 60

    @classmethod
    def validate(cls) -> bool:
        if not cls.GEMINI_API_KEY:
            return False
        return True

    @classmethod
    def get_api_key(cls) -> str:
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "Gemini API key not found\n"
                "Get your key at: https://aistudio.google.com/app/apikey"
            )
        return cls.GEMINI_API_KEY

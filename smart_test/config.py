"""Configuration management for Smart Test Generator"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')
    
    # Test Generation Defaults
    DEFAULT_FRAMEWORK: str = 'pytest'
    DEFAULT_OUTPUT_DIR: str = 'tests'
    DEFAULT_TEST_PREFIX: str = 'test_'
    
    # Coverage Settings
    MIN_COVERAGE: int = 80
    
    # File Patterns
    PYTHON_EXTENSIONS: tuple = ('.py',)
    EXCLUDE_PATTERNS: tuple = (
        '__pycache__',
        '.pytest_cache',
        '.venv',
        'venv',
        'env',
        '.git',
        'build',
        'dist',
        '*.egg-info',
        'test_*',
        '*_test.py'
    )
    
    # Generation Settings
    MAX_RETRIES: int = 3
    TIMEOUT: int = 60
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.GEMINI_API_KEY:
            return False
        return True
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get API key with validation"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY in .env file or environment variable.\n"
                "Get your key at: https://aistudio.google.com/app/apikey"
            )
        return cls.GEMINI_API_KEY
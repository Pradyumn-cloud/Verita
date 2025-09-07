from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional
import json
import yaml
import toml
from contextlib import contextmanager

PYTHON_GLOB = "*.py"
CONFIG_FILENAMES = ["smart_test.json", "smart_test.yaml", "smart_test.toml", "pyproject.toml"]

def iter_python_files(root: str | Path) -> Iterable[Path]:
    """Iterate through Python files in a project, skipping typical venv directories."""
    base = Path(root)
    
    # Skip these directories
    skip_dirs = {
        "venv", "env", ".venv", ".env", ".git", 
        "__pycache__", "build", "dist", ".pytest_cache", 
        ".mypy_cache", ".tox", ".eggs", "*.egg-info"
    }
    
    for path in base.rglob(PYTHON_GLOB):
        # Check if this file should be skipped
        parts = path.parts
        skip = False
        for part in parts:
            if any(part == skip_dir or (skip_dir.startswith("*.") and part.endswith(skip_dir[1:])) 
                   for skip_dir in skip_dirs):
                skip = True
                break
        
        if not skip:
            yield path

def read_text(path: Path) -> str:
    """Read text from a file with robust encoding handling."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fall back to alternative encoding
        return path.read_text(encoding="latin-1", errors="replace")
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def find_config_file(root: Path) -> Optional[Path]:
    """Find a configuration file in the project root."""
    for filename in CONFIG_FILENAMES:
        config_path = root / filename
        if config_path.exists():
            return config_path
    return None

def load_config(root: Path) -> Dict[str, Any]:
    """Load configuration from a config file."""
    config_path = find_config_file(root)
    if not config_path:
        return {}  # Default empty config
        
    try:
        content = read_text(config_path)
        if str(config_path).endswith(".json"):
            return json.loads(content)
        elif str(config_path).endswith((".yaml", ".yml")):
            return yaml.safe_load(content) or {}
        elif str(config_path).endswith(".toml"):
            # For pyproject.toml, look for [tool.smart-test] section
            config = toml.loads(content)
            if config_path.name == "pyproject.toml":
                return config.get("tool", {}).get("smart-test", {})
            return config
    except Exception as e:
        print(f"Error loading config from {config_path}: {e}")
        
    return {}

def create_directory_if_not_exists(path: Path) -> None:
    """Create a directory if it doesn't exist."""
    if not path.exists():
        path.mkdir(parents=True)

@contextmanager
def safe_write_file(path: Path):
    """Safely write a file by writing to a temporary file first."""
    from tempfile import NamedTemporaryFile
    import os
    import shutil
    
    # Create parent directory if it doesn't exist
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        
    # Create a temporary file in the same directory
    with NamedTemporaryFile(mode='w', delete=False, dir=path.parent) as temp:
        try:
            yield temp
            temp.flush()
            os.fsync(temp.fileno())
            
            # Close the file and rename it to the target path
            temp_name = temp.name
        except Exception:
            # Close and remove the temporary file on error
            temp_name = temp.name
            raise
            
    # Move the temp file to the target path
    shutil.move(temp_name, path)
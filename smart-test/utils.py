from pathlib import Path
from typing import Iterable, List

PYTHON_GLOB = "*.py"

def iter_python_files(root: str | Path) -> Iterable[Path]:
    base = Path(root)
    # Skip typical virtualenv/build dirs if desired later
    return base.rglob(PYTHON_GLOB)

def read_text(path: Path) -> str:
    # Robust read with UTF-8 default
    return path.read_text(encoding="utf-8", errors="replace")

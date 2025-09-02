from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple
from .utils import iter_python_files, read_text

@dataclass(frozen=True)

class FunctionInfo:
    file: Path
    module_rel: Path
    qualname: str
    lineno: int
    hasTest: bool

def _functions_in_ast(tree:ast.AST) -> List[Tuple[str, int]]:
    results: List[Tuple[str, int]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            results.append((node.name, node.lineno))
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    results.append((f"{node.name}.{item.name}", item.lineno))
    return results

def _likely_test_files(root: Path) -> List[Path]:
    tests_dir = root / "tests"
    patterns = ["test_*.py", "*_test.py"]
    files: List[Path] = []
    if tests_dir.exists():
        for pat in patterns:
            files.extend(tests_dir.rglob(pat))
    return files

def _has_tests_for(module_rel: Path, func_name: str, test_files: List[Path]) -> bool:
    mod_base = module_rel.stem
    for tf in test_files:
        name = tf.stem
        if mod_base in name:
            return True
    return False

def analyze_project(root: str | Path) -> List[FunctionInfo]:
    root = Path(root).resolve()
    test_files = _likely_test_files(root)
    results: List[FunctionInfo] = []

    for file_path in iter_python_files(root):
        rel = file_path.relative_to(root)
        if str(rel).startswith("tests/"):
            continue
        try:
            src = read_text(file_path)
            tree = ast.parse(src, filename=str(file_path))  # [9]
        except Exception:
            continue

        for qualname, lineno in _functions_in_ast(tree):
            has_tests = _has_tests_for(rel, qualname, test_files)
            results.append(FunctionInfo(
                file=file_path,
                module_rel=rel,
                qualname=qualname,
                lineno=lineno,
                has_tests=has_tests,
            ))
    return results
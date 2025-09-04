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
    has_tests: bool
    covered: bool = False

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

def parse_coverage_xml(xml_path: str) -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    file_coverage = {}
    for class_node in root.findall(".//class"):
        filename = class_node.attrib["filename"]
        covered_lines = set(
            int(line.attrib["number"])
            for line in class_node.findall("lines/line")
            if int(line.attrib["hits"]) > 0
        )
        file_coverage[filename] = covered_lines
    return file_coverage

def map_coverage_to_functions(functions, file_coverage):
    for fi in functions:
        rel_path = str(fi.module_rel)
        covered_lines = file_coverage.get(rel_path, set())
        if fi.lineno in covered_lines:
            object.__setattr__(fi, "covered", True)
    return functions

def summarize_coverage(functions):
    need_tests = [fi for fi in functions if not fi.has_tests or not fi.covered]
    priority_funcs = [fi.qualname for fi in need_tests[:3]]
    low_coverage_files = {fi.module_rel for fi in functions if not fi.covered}
    return {
        "need_tests_count": len(need_tests),
        "low_coverage_count": len(low_coverage_files),
        "priority_functions": priority_funcs,
    }

from __future__ import annotations
import ast
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Dict, Set, Optional
from .utils import iter_python_files, read_text

@dataclass(frozen=True)
class FunctionInfo:
    file: Path
    module_rel: Path
    qualname: str
    lineno: int
    has_tests: bool
    covered: bool = False

def _functions_in_ast(tree: ast.AST) -> List[Tuple[str, int]]:
    results: List[Tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get parent class if it exists
            parent_class = None
            for potential_parent in ast.walk(tree):
                if isinstance(potential_parent, ast.ClassDef) and node in potential_parent.body:
                    parent_class = potential_parent.name
                    break
            
            if parent_class:
                results.append((f"{parent_class}.{node.name}", node.lineno))
            else:
                results.append((node.name, node.lineno))
    
    return results

def _likely_test_files(root: Path) -> List[Path]:
    """Find likely test files in the project."""
    tests_dir = root / "tests"
    patterns = ["test_*.py", "*_test.py"]
    files: List[Path] = []
    
    # Look in tests directory
    if tests_dir.exists():
        for pat in patterns:
            files.extend(tests_dir.rglob(pat))
    
    # Also look for tests in the main package
    for pat in patterns:
        files.extend(root.rglob(pat))
        
    return files

def _has_tests_for(module_rel: Path, func_name: str, test_files: List[Path]) -> bool:
    """Check if tests exist for a specific function."""
    mod_base = module_rel.stem
    class_name = None
    method_name = None
    
    # Handle class methods
    if "." in func_name:
        class_name, method_name = func_name.split(".", 1)
    else:
        method_name = func_name
    
    for tf in test_files:
        # Check if the test file is named appropriately
        if mod_base in tf.stem or (class_name and class_name.lower() in tf.stem.lower()):
            content = read_text(tf)
            # Check for test_function_name pattern
            if f"test_{method_name}" in content or f"test_{func_name}" in content:
                return True
            # Check for TestClass pattern
            if class_name and f"Test{class_name}" in content:
                return True
    
    return False

def analyze_project(root: str | Path) -> List[FunctionInfo]:
    """Analyze a Python project to find functions and their test status."""
    root = Path(root).resolve()
    test_files = _likely_test_files(root)
    results: List[FunctionInfo] = []

    for file_path in iter_python_files(root):
        rel = file_path.relative_to(root)
        # Skip test files
        if str(rel).startswith("tests/") or any(pattern in str(rel) for pattern in ["test_", "_test"]):
            continue
            
        try:
            src = read_text(file_path)
            tree = ast.parse(src, filename=str(file_path))
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            continue

        for qualname, lineno in _functions_in_ast(tree):
            # Skip private methods, dunder methods
            if qualname.startswith("_") and not qualname.startswith("__init__"):
                continue
                
            has_tests = _has_tests_for(rel, qualname, test_files)
            results.append(FunctionInfo(
                file=file_path,
                module_rel=rel,
                qualname=qualname,
                lineno=lineno,
                has_tests=has_tests,
            ))
            
    return results

def parse_coverage_xml(xml_path: str) -> Dict[str, Set[int]]:
    """Parse a coverage.py XML report to extract covered lines."""
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

def map_coverage_to_functions(functions: List[FunctionInfo], 
                             file_coverage: Dict[str, Set[int]]) -> List[FunctionInfo]:
    """Map coverage information to function objects."""
    for fi in functions:
        rel_path = str(fi.module_rel)
        covered_lines = file_coverage.get(rel_path, set())
        if fi.lineno in covered_lines:
            object.__setattr__(fi, "covered", True)
            
    return functions

def summarize_coverage(functions: List[FunctionInfo]) -> Dict[str, any]:
    """Summarize coverage information for reporting."""
    need_tests = [fi for fi in functions if not fi.has_tests or not fi.covered]
    priority_funcs = sorted([fi for fi in need_tests], 
                           key=lambda x: not x.qualname.startswith("__init__"))[:5]
    
    low_coverage_files = {fi.module_rel for fi in functions if not fi.covered}
    
    return {
        "need_tests_count": len(need_tests),
        "low_coverage_count": len(low_coverage_files),
        "priority_functions": [fi.qualname for fi in priority_funcs],
        "untested_functions": need_tests,
    }

def generate_test_skeleton(function_info: FunctionInfo, root: Path) -> Optional[str]:
    """Generate a test skeleton for a given function."""
    import inspect
    import importlib.util
    
    # Try to import the module to get function signature
    try:
        module_path = function_info.file
        module_name = function_info.module_rel.stem
        
        # Create module spec and load module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the function in the module
        func_parts = function_info.qualname.split('.')
        obj = module
        
        for part in func_parts:
            obj = getattr(obj, part, None)
            if obj is None:
                break
                
        if obj and callable(obj):
            # Get function signature
            sig = inspect.signature(obj)
            param_list = []
            
            for name, param in sig.parameters.items():
                if name == 'self':
                    continue
                param_list.append(name)
                
            # Generate test skeleton
            test_name = f"test_{function_info.qualname.replace('.', '_')}"
            
            if len(func_parts) > 1:  # It's a method
                class_name = func_parts[0]
                test_code = [
                    f"def {test_name}():",
                    f"    # Setup",
                    f"    instance = {class_name}()",
                    f"    # Exercise",
                ]
                
                if param_list:
                    params_str = ", ".join(f"{p}=None" for p in param_list)
                    test_code.append(f"    result = instance.{func_parts[1]}({params_str})")
                else:
                    test_code.append(f"    result = instance.{func_parts[1]}()")
            else:
                # It's a regular function
                test_code = [
                    f"def {test_name}():",
                    f"    # Setup",
                ]
                
                if param_list:
                    params_str = ", ".join(f"{p}=None" for p in param_list)
                    test_code.append(f"    result = {function_info.qualname}({params_str})")
                else:
                    test_code.append(f"    result = {function_info.qualname}()")
            
            test_code.extend([
                "    # Verify",
                "    assert result is not None  # Replace with actual assertion",
                "    # Cleanup - Add any necessary cleanup code here"
            ])
            
            return "\n".join(test_code)
            
    except Exception as e:
        print(f"Error generating test for {function_info.qualname}: {e}")
        
    # Fallback simple test skeleton
    test_name = f"test_{function_info.qualname.replace('.', '_')}"
    return "\n".join([
        f"def {test_name}():",
        f"    # TODO: Implement test for {function_info.qualname}",
        f"    assert True  # Replace with actual test"
    ])
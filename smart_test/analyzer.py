"""Python code analyzer for test generation"""

import ast
from typing import List
from pathlib import Path
from .models import FunctionInfo, AnalysisResult
from .utils import read_text
from typing import Optional


class CodeAnalyzer:
    """Analyzes Python source code to extract testable components"""

    def __init__(self):
        self.functions: List[FunctionInfo] = []
        self.imports: List[str] = []
        self.classes: List[str] = []

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a Python file and extract all testable functions

        Args:
            file_path: Path to Python file

        Returns:
            AnalysisResult containing all extracted information
        """
        content = read_text(Path(file_path))

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in {file_path}: {e}")

        # Extract components
        self.imports = self._extract_imports(tree)
        self.classes = self._extract_classes(tree)
        self.functions = self._extract_functions(tree, content)

        # Calculate metrics
        total_complexity = sum(f.complexity for f in self.functions)
        avg_complexity = total_complexity / len(self.functions) if self.functions else 0

        return AnalysisResult(
            file_path=file_path,
            functions=self.functions,
            imports=self.imports,
            classes=self.classes,
            total_functions=len(self.functions),
            total_complexity=total_complexity,
            average_complexity=round(avg_complexity, 2),
        )

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all import statements"""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = ", ".join([alias.name for alias in node.names])
                imports.append(f"from {module} import {names}")

        return imports

    def _extract_classes(self, tree: ast.AST) -> List[str]:
        """Extract all class names"""
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return classes

    def _extract_functions(self, tree: ast.AST, source: str) -> List[FunctionInfo]:
        """Extract all function definitions"""
        source_lines = source.split("\n")

        class FunctionVisitor(ast.NodeVisitor):
            def __init__(self):
                self.functions: List[FunctionInfo] = []
                self.current_class: Optional[str] = None

            def visit_ClassDef(self, node):
                old_class = self.current_class
                self.current_class = node.name
                self.generic_visit(node)
                self.current_class = old_class

            def visit_FunctionDef(self, node):
                self._process_function(node, is_async=False)

            def visit_AsyncFunctionDef(self, node):
                self._process_function(node, is_async=True)

            def _process_function(self, node: ast.FunctionDef, is_async: bool):
                # Skip private test functions
                if node.name.startswith("test_"):
                    return

                # Get function source
                start = node.lineno - 1
                end = node.end_lineno if hasattr(node, "end_lineno") else start + 10
                func_source = "\n".join(source_lines[start:end])

                # Get parameters (exclude self/cls)
                params = [arg.arg for arg in node.args.args]
                if params and params[0] in ("self", "cls"):
                    params = params[1:]

                # Get docstring
                docstring = ast.get_docstring(node)

                # Get return type
                return_type = None
                if node.returns:
                    try:
                        return_type = ast.unparse(node.returns)
                    except:
                        return_type = str(node.returns)

                # Get decorators
                decorators = []
                for dec in node.decorator_list:
                    try:
                        decorators.append(ast.unparse(dec))
                    except:
                        decorators.append(str(dec))

                # Calculate complexity
                complexity = self._calculate_complexity(node)

                func_info = FunctionInfo(
                    name=node.name,
                    params=params,
                    docstring=docstring,
                    source=func_source,
                    return_type=return_type,
                    line_number=node.lineno,
                    complexity=complexity,
                    is_async=is_async,
                    decorators=decorators,
                    class_name=self.current_class,
                )

                self.functions.append(func_info)

            def _calculate_complexity(self, node: ast.FunctionDef) -> int:
                """Calculate cyclomatic complexity"""
                complexity = 1

                for child in ast.walk(node):
                    if isinstance(
                        child,
                        (
                            ast.If,
                            ast.While,
                            ast.For,
                            ast.Try,
                            ast.With,
                            ast.ExceptHandler,
                        ),
                    ):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1

                return complexity

        visitor = FunctionVisitor()
        visitor.visit(tree)
        return visitor.functions

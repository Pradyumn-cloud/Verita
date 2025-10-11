"""Data models for Smart Test Generator"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum

class TestFramework(Enum):
    """Supported test frameworks"""
    PYTEST = "pytest"
    UNITTEST = "unittest"

class TestPriority(Enum):
    """Test priority levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class FunctionInfo:
    """Information about a detected function"""
    name: str
    params: List[str]
    docstring: Optional[str]
    source: str
    return_type: Optional[str] = None
    line_number: int = 0
    complexity: int = 0
    is_async: bool = False
    decorators: List[str] = field(default_factory=list)
    class_name: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'params': self.params,
            'docstring': self.docstring,
            'source': self.source,
            'return_type': self.return_type,
            'line_number': self.line_number,
            'complexity': self.complexity,
            'is_async': self.is_async,
            'decorators': self.decorators,
            'class_name': self.class_name
        }

@dataclass
class TestGenerationConfig:
    """Configuration for test generation"""
    framework: TestFramework = TestFramework.PYTEST
    use_ai: bool = True
    coverage_threshold: int = 80
    include_mocks: bool = True
    include_fixtures: bool = True
    include_parametrize: bool = True
    verbose: bool = False
    
@dataclass
class AnalysisResult:
    """Result of code analysis"""
    file_path: str
    functions: List[FunctionInfo]
    imports: List[str]
    classes: List[str]
    total_functions: int
    total_complexity: int
    average_complexity: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'file_path': self.file_path,
            'functions': [f.to_dict() for f in self.functions],
            'imports': self.imports,
            'classes': self.classes,
            'total_functions': self.total_functions,
            'total_complexity': self.total_complexity,
            'average_complexity': self.average_complexity
        }
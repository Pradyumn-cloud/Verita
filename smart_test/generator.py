#for test file generation
from pathlib import Path
from typing import Optional
from .models import AnalysisResult, TestFramework, TestGenerationConfig
from .llm_client import LLMClient
from .analyzer import CodeAnalyzer

class TestGenerator:
    
    def __init__(self, config: TestGenerationConfig):
        self.config = config
        self.analyzer = CodeAnalyzer()
        self.llm_client = LLMClient() if config.use_ai else None
    
    def generate_test_file(
        self,
        source_file: str,
        output_file: Optional[str] = None
    ) -> str:
        """Generate test file for source code
        
        Args:
            source_file: Path to source Python file
            output_file: Optional output path (auto-generated if None)
            
        Returns:
            Path to generated test file
        """
        analysis = self.analyzer.analyze_file(source_file)
        
        if not analysis.functions:
            raise ValueError(f"No testable functions found in {source_file}")
        if not output_file:
            output_file = self._get_default_output_path(source_file)

        if self.config.use_ai and self.llm_client:
            test_content = self.llm_client.generate_test_file(
                functions=analysis.functions,
                source_file=source_file,
                imports=analysis.imports,
                framework=self.config.framework
            )
        else:
            test_content = self._generate_basic_tests(analysis)
       
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(test_content, encoding='utf-8')
        
        return str(output_path)
    
    def _get_default_output_path(self, source_file: str) -> str:
        """Generate default output path for test file"""
        source_path = Path(source_file)
        test_filename = f"test_{source_path.name}"
        
        if source_path.parent.name and source_path.parent.name != '.':

            test_dir = source_path.parent.parent / 'tests'
        else:

            test_dir = source_path.parent / 'tests'
        
        return str(test_dir / test_filename)
    
    def _generate_basic_tests(self, analysis: AnalysisResult) -> str:
        """Generate basic test file without AI"""
        module_name = Path(analysis.file_path).stem
        
        lines = [
            f'"""Tests for {analysis.file_path}"""',
            '',
            'import pytest',
            f'from {module_name} import *',
            '',
            ''
        ]
        
        for func in analysis.functions:
            class_prefix = f"{func.class_name}_" if func.class_name else ""
            
            lines.extend([
                f'def test_{class_prefix}{func.name}_basic():',
                f'    """Test {func.name} basic functionality"""',
                f'    # TODO: Implement test for {func.name}',
                f'    # Parameters: {", ".join(func.params) if func.params else "None"}',
                f'    # Return type: {func.return_type or "Unknown"}',
                f'    pass',
                '',
                ''
            ])
        
        return '\n'.join(lines)
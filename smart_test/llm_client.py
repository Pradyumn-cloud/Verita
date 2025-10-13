from typing import Optional, List
from .models import FunctionInfo, TestFramework
from .config import Config

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "install - pip install google-generativeai"
    )


class LLMClient:

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize LLM client

        Args:
            api_key
            model name
        """
        self.api_key = api_key or Config.get_api_key()
        self.model_name = model or Config.GEMINI_MODEL

        genai.configure(api_key=self.api_key)

        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }

        self.model = genai.GenerativeModel(
            model_name=self.model_name, generation_config=self.generation_config
        )

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

    def generate_test_file(
        self,
        functions: List[FunctionInfo],
        source_file: str,
        imports: List[str],
        framework: TestFramework = TestFramework.PYTEST,
    ) -> str:
        """
        Args:
            functions: List of functions
            source_file: Path to source file being tested
            imports: List of import statements from source
            framework: Test framework to use

        Returns:
            Complete test file content as string
        """
        prompt = self._build_test_file_prompt(
            functions, source_file, imports, framework
        )

        try:
            response = self.model.generate_content(
                prompt, safety_settings=self.safety_settings
            )

            if response.text:
                return self._extract_code(response.text)

            return self._generate_fallback_tests(functions, source_file, framework)

        except Exception as e:
            print(f"Error generating tests with AI: {e}")
            return self._generate_fallback_tests(functions, source_file, framework)

    def _build_test_file_prompt(
        self,
        functions: List[FunctionInfo],
        source_file: str,
        imports: List[str],
        framework: TestFramework,
    ) -> str:

        functions_summary = "\n\n".join(
            [
                f"### Function: {func.name}\n"
                f"- Parameters: {', '.join(func.params) or 'None'}\n"
                f"- Return Type: {func.return_type or 'Not specified'}\n"
                f"- Complexity: {func.complexity}\n"
                f"- Is Async: {func.is_async}\n"
                f"- Class: {func.class_name or 'Standalone'}\n"
                f"- Docstring: {func.docstring or 'No documentation'}\n"
                f"```python\n{func.source}\n```"
                for func in functions
            ]
        )

        imports_str = "\n".join(imports) if imports else "# No imports detected"

        return f"""You are an expert Python test engineer. {framework.value}.

**SOURCE FILE:** `{source_file}`

**DETECTED IMPORTS:**
```python
{imports_str}
```

**FUNCTIONS TO TEST:**
{functions_summary}

**REQUIREMENTS:**

1. **Test File Structure:**
   - Start with proper docstring describing what's being tested
   - Import {framework.value} and all necessary testing utilities
   - Import the source module correctly
   - Use absolute imports when possible

2. **Test Coverage (Aim for 100%):**
   - Test happy path (valid inputs, expected behavior)
   - Test edge cases (boundary values, empty inputs, None)
   - Test error cases (invalid inputs, exceptions)
   - Test all parameters and return values
   - Test class methods with proper setup/teardown
   - Test async functions with async test markers

3. **Test Organization:**
   - Group tests by function using test classes
   - Use descriptive test names: test_<function>_<scenario>_<expected_result>
   - Use fixtures for repeated setup
   - Use parametrize for data-driven tests
   - Add clear comments explaining complex test logic

4. **Mocking & Fixtures:**
   - Mock external dependencies (APIs, databases, files)
   - Use pytest fixtures for test data
   - Mock datetime, random for deterministic tests
   - Use monkeypatch for environment variables

5. **Best Practices:**
   - Follow PEP 8 style guide
   - Use assert statements with clear messages
   - Test one thing per test function
   - Make tests independent (no shared state)
   - Use setup/teardown appropriately

6. **Output Format:**
   - Return ONLY Python code, no explanations
   - Code must be ready to run: pytest test_file.py
   - Include all necessary imports
   - Use proper indentation (4 spaces)

**Generate the complete test file now:**
"""

    def _extract_code(self, response_text: str) -> str:
        """Extract Python code from AI response"""
        # Remove markdown code blocks
        if "```python" in response_text:
            parts = response_text.split("```python")
            if len(parts) > 1:
                code = parts[1].split("```")[0]
                return code.strip()

        if "```" in response_text:
            parts = response_text.split("```")
            if len(parts) >= 2:
                return parts[1].strip()

        return response_text.strip()

    def _generate_fallback_tests(
        self, functions: List[FunctionInfo], source_file: str, framework: TestFramework
    ) -> str:
        """Generate basic tests without AI (fallback)"""
        from pathlib import Path

        module_name = Path(source_file).stem

        lines = [
            f'"""Tests for {source_file}"""',
            "",
            "import pytest",
            f"from {module_name} import *",
            "",
            "",
        ]

        for func in functions:
            lines.extend(
                [
                    f"def test_{func.name}_basic():",
                    f'    """Test {func.name} with basic inputs"""',
                    "    # TODO: Add test implementation",
                    "    pass",
                    "",
                    "",
                ]
            )

        return "\n".join(lines)

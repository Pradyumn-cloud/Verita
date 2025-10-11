# 📚 Smart Test Generator - Complete Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation & Setup](#installation--setup)
4. [Getting Started](#getting-started)
5. [Command Reference](#command-reference)
6. [Configuration](#configuration)
7. [Advanced Usage](#advanced-usage)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Introduction

**Smart Test Generator** is an AI-powered tool that automatically generates comprehensive test files for your Python projects. It uses Google's Gemini AI to analyze your code and create intelligent, meaningful test cases that cover:

- Basic functionality
- Edge cases
- Error handling
- Type validation
- Complex scenarios

### What Makes It Smart?

- 🧠 **AI Analysis**: Understands your code's logic and purpose
- 🎯 **Context-Aware**: Generates relevant test cases based on code complexity
- 📦 **Scalable**: Process single files or entire projects
- 🔧 **Flexible**: Supports pytest and unittest frameworks
- ⚡ **Fast**: Efficient async processing with Google Gemini API

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python Version**: 3.8 or higher
- **RAM**: 2GB minimum
- **Internet Connection**: Required for Gemini API calls

### Required Software

- Python 3.8+
- pip (Python package manager)
- Git (for cloning the repository)

### Dependencies

All dependencies are automatically installed via `setup.py`:

```
google-generativeai >= 0.3.0
python-dotenv >= 0.19.0
click >= 8.0.0
radon >= 5.1.0
```

---

## Installation & Setup

### Step 1: Clone the Repository

Open your terminal and run:

```bash
# Clone from GitHub
git clone https://github.com/Pradyumn-cloud/Verita.git

# Navigate to project directory
cd Verita
```

### Step 2: Verify Python Version

Ensure you have Python 3.8 or higher:

```bash
# Check Python version
python --version

# or
python3 --version
```

Expected output: `Python 3.8.x` or higher

### Step 3: Install the Package

Install Smart Test Generator in editable mode:

```bash
# Install with all dependencies
pip install -e .
```

**What this does:**
- Installs the `smart_test` package
- Installs all required dependencies
- Creates the `smart-test` command-line tool
- Sets up in editable mode (changes to source code reflect immediately)

### Step 4: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy the generated API key

**Note:** The free tier includes generous usage limits suitable for most projects.

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# On Windows (PowerShell)
New-Item .env -ItemType File

# On Linux/macOS
touch .env
```

Open `.env` and add your API key:

```env
# Required: Your Gemini API Key
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Optional: Custom model (default: gemini-1.5-flash)
GEMINI_MODEL=gemini-1.5-flash

# Optional: Request timeout in seconds (default: 30)
TIMEOUT=30

# Optional: Max retries for API calls (default: 3)
MAX_RETRIES=3
```

### Step 6: Verify Installation

Test that the installation was successful:

```bash
# Check if command is available
smart-test --help
```

You should see the help menu with all available commands.

### Step 7: Test with Example

Run the tool on an example file:

```bash
# Generate test for calculator example
smart-test generate examples/calculator.py

# Check the output
ls test_*.py
```

---

## Getting Started

### Your First Test Generation

Let's create a simple Python file and generate tests for it.

#### 1. Create a Sample Python File

Create `my_math.py`:

```python
def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def is_even(num):
    """Check if a number is even."""
    return num % 2 == 0

def factorial(n):
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

#### 2. Generate Tests

```bash
smart-test generate my_math.py
```

**Output:**
```
✓ Analyzing code structure...
✓ Generating AI-powered tests...
✓ Test file created: test_my_math.py
```

#### 3. Review Generated Tests

Open `test_my_math.py` to see:
- Test cases for basic functionality
- Edge case tests (negative numbers, zero, etc.)
- Error handling tests
- Proper pytest fixtures and assertions

#### 4. Run the Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run the generated tests
pytest test_my_math.py -v
```

---

## Command Reference

### Global Command Structure

```bash
smart-test [COMMAND] [SOURCE] [OPTIONS]
```

---

### Command 1: `generate`

**Purpose:** Generate a comprehensive test file for a Python source file.

#### Basic Syntax

```bash
smart-test generate <source_file> [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_file` | Path | ✅ Yes | Path to the Python file to test |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | Path | `test_<source>.py` | Custom output file path |
| `--framework` | `-f` | Choice | `pytest` | Test framework (`pytest` or `unittest`) |
| `--no-ai` | - | Flag | `False` | Generate basic template without AI |
| `--api-key` | `-k` | String | From `.env` | Override API key |
| `--verbose` | `-v` | Flag | `False` | Enable detailed logging |

#### Examples

**Example 1: Basic Generation**
```bash
smart-test generate calculator.py
# Output: test_calculator.py
```

**Example 2: Custom Output Path**
```bash
smart-test generate src/utils.py -o tests/test_utils.py
# Output: tests/test_utils.py
```

**Example 3: Use unittest Framework**
```bash
smart-test generate app.py -f unittest
# Generates unittest-style tests instead of pytest
```

**Example 4: Generate Without AI**
```bash
smart-test generate complex_module.py --no-ai
# Creates basic test template structure only
```

**Example 5: Verbose Mode**
```bash
smart-test generate mycode.py -v
# Shows detailed progress and API calls
```

**Example 6: Override API Key**
```bash
smart-test generate mycode.py -k "AIzaSyXXXXXXXXXXXXXXXX"
# Uses provided API key instead of .env file
```

#### What Gets Generated?

The generated test file includes:

1. **Proper Imports**
   ```python
   import pytest
   from mymodule import function_name
   ```

2. **Test Functions**
   ```python
   def test_function_basic():
       """Test basic functionality."""
       assert function(input) == expected
   ```

3. **Edge Cases**
   ```python
   def test_function_edge_cases():
       """Test edge cases."""
       assert function(0) == expected
       assert function(-1) == expected
   ```

4. **Error Handling**
   ```python
   def test_function_error_handling():
       """Test error conditions."""
       with pytest.raises(ValueError):
           function(invalid_input)
   ```

5. **Fixtures (if needed)**
   ```python
   @pytest.fixture
   def sample_data():
       return {"key": "value"}
   ```

---

### Command 2: `analyze`

**Purpose:** Analyze Python code and get insights without generating tests.

#### Basic Syntax

```bash
smart-test analyze <source_file> [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_file` | Path | ✅ Yes | Path to Python file to analyze |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--verbose` | `-v` | Flag | `False` | Show detailed analysis |

#### Examples

**Example 1: Basic Analysis**
```bash
smart-test analyze calculator.py
```

**Output:**
```
📊 Code Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: calculator.py
Complexity: Medium (Score: 4.2)

Functions Detected:
  ✓ add(a, b)
  ✓ subtract(a, b)
  ✓ multiply(a, b)
  ✓ divide(a, b)

Classes Detected:
  ✓ Calculator

Recommended Test Strategy:
  • Unit tests for each arithmetic operation
  • Edge case tests for division by zero
  • Type validation tests
  • Integration tests for Calculator class

Test Coverage Suggestions:
  • Basic functionality: 4 tests
  • Edge cases: 3 tests
  • Error handling: 2 tests
  Estimated total: 9 test cases
```

**Example 2: Verbose Analysis**
```bash
smart-test analyze complex_app.py -v
```

Shows additional details:
- Cyclomatic complexity for each function
- Import dependencies
- Code metrics
- Detailed recommendations

#### Use Cases

1. **Before Test Generation**: Understand code structure
2. **Code Review**: Get complexity metrics
3. **Refactoring Planning**: Identify complex functions
4. **Test Planning**: See recommended test strategies

---

### Command 3: `batch`

**Purpose:** Generate tests for multiple Python files in a directory.

#### Basic Syntax

```bash
smart-test batch <source_directory> [OPTIONS]
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_directory` | Path | ✅ Yes | Directory containing Python files |

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--output` | `-o` | Path | Same dir | Output directory for test files |
| `--framework` | `-f` | Choice | `pytest` | Test framework |
| `--verbose` | `-v` | Flag | `False` | Detailed progress |
| `--recursive` | `-r` | Flag | `False` | Process subdirectories |

#### Examples

**Example 1: Basic Batch Processing**
```bash
smart-test batch src/
# Generates test files in src/ directory
```

**Example 2: Custom Output Directory**
```bash
smart-test batch src/ -o tests/
# Saves all test files to tests/ directory
# Creates: tests/test_module1.py, tests/test_module2.py, etc.
```

**Example 3: Recursive Processing**
```bash
smart-test batch src/ -o tests/ -r
# Processes all Python files in src/ and subdirectories
# Maintains directory structure in tests/
```

**Example 4: Batch with unittest**
```bash
smart-test batch myproject/ -o tests/ -f unittest
# All generated tests use unittest framework
```

**Example 5: Verbose Batch**
```bash
smart-test batch src/ -o tests/ -v
# Shows progress for each file:
# [1/5] Processing src/module1.py... ✓
# [2/5] Processing src/module2.py... ✓
# ...
```

#### Behavior

- **Skips existing test files**: Won't overwrite `test_*.py` files
- **Maintains structure**: With `-r`, recreates directory hierarchy
- **Error handling**: Continues processing even if one file fails
- **Progress reporting**: Shows completion status for each file

---

## Configuration

### Environment Variables (.env)

The `.env` file controls API and runtime settings:

```env
# ============================================
# REQUIRED SETTINGS
# ============================================

# Your Google Gemini API Key (REQUIRED)
GEMINI_API_KEY=your_actual_api_key_here

# ============================================
# OPTIONAL SETTINGS
# ============================================

# Gemini Model Selection
# Options: gemini-1.5-flash, gemini-1.5-pro
# Default: gemini-1.5-flash (faster, cheaper)
GEMINI_MODEL=gemini-1.5-flash

# API Request Timeout (seconds)
# Default: 30
TIMEOUT=30

# Maximum API Retry Attempts
# Default: 3
MAX_RETRIES=3

# Temperature for AI Generation (0.0 - 1.0)
# Lower = more focused, Higher = more creative
# Default: 0.7
TEMPERATURE=0.7

# Maximum tokens in AI response
# Default: 2048
MAX_TOKENS=2048
```

### Configuration File (config.py)

Advanced users can modify `smart_test/config.py`:

```python
# API Settings
DEFAULT_MODEL = "gemini-1.5-flash"
MAX_RETRIES = 3
TIMEOUT = 30

# Generation Settings
DEFAULT_FRAMEWORK = "pytest"
TEMPERATURE = 0.7
MAX_TOKENS = 2048

# Analysis Settings
COMPLEXITY_THRESHOLDS = {
    "low": 5,
    "medium": 10,
    "high": float("inf")
}
```

---

## Advanced Usage

### 1. Custom Test Templates

Modify generation behavior by editing `smart_test/generator.py`:

```python
# Customize test template
TEMPLATE = """
import pytest
from {module} import *

# Custom header comment
# Generated by Smart Test Generator

{test_functions}
"""
```

### 2. Framework-Specific Options

#### pytest Configuration

Create `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

#### unittest Configuration

Generated unittest tests include:

```python
import unittest

class TestMyModule(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_function(self):
        """Test case."""
        self.assertEqual(result, expected)
    
    def tearDown(self):
        """Clean up after tests."""
        pass

if __name__ == '__main__':
    unittest.main()
```

### 3. Integration with CI/CD

#### GitHub Actions Example

Create `.github/workflows/test.yml`:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest
      - name: Generate tests
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: smart-test batch src/ -o tests/
      - name: Run tests
        run: pytest tests/
```

### 4. Custom AI Prompts

Modify prompts in `smart_test/llm_client.py`:

```python
SYSTEM_PROMPT = """
You are an expert Python test engineer.
Generate comprehensive, production-ready test cases.
Focus on: edge cases, error handling, type safety.
"""
```

---

## API Reference

### Python API Usage

You can use Smart Test Generator programmatically:

```python
from smart_test.generator import TestGenerator
from smart_test.analyzer import CodeAnalyzer
from smart_test.config import Config

# Initialize configuration
config = Config(api_key="your_api_key")

# Analyze code
analyzer = CodeAnalyzer("mymodule.py")
analysis = analyzer.analyze()
print(f"Complexity: {analysis.complexity}")
print(f"Functions: {analysis.functions}")

# Generate tests
generator = TestGenerator(config)
test_code = generator.generate(
    source_file="mymodule.py",
    framework="pytest",
    use_ai=True
)

# Save to file
with open("test_mymodule.py", "w") as f:
    f.write(test_code)
```

### Core Classes

#### TestGenerator

```python
class TestGenerator:
    def __init__(self, config: Config):
        """Initialize test generator."""
        
    def generate(self, source_file: str, framework: str = "pytest", 
                 use_ai: bool = True) -> str:
        """Generate test code."""
        
    def generate_batch(self, directory: str, output_dir: str,
                       framework: str = "pytest") -> List[str]:
        """Generate tests for directory."""
```

#### CodeAnalyzer

```python
class CodeAnalyzer:
    def __init__(self, source_file: str):
        """Initialize analyzer."""
        
    def analyze(self) -> AnalysisResult:
        """Analyze code structure."""
        
    def get_complexity(self) -> float:
        """Calculate cyclomatic complexity."""
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Command Not Found

**Error:**
```
'smart-test' is not recognized as an internal or external command
```

**Solution:**
```bash
# Reinstall the package
pip install -e .

# Verify Python Scripts directory is in PATH
# Windows: Add to PATH: C:\Python3X\Scripts
# Linux/macOS: Usually automatic
```

#### Issue 2: API Key Not Found

**Error:**
```
Error: GEMINI_API_KEY not found in environment
```

**Solution:**
1. Verify `.env` file exists in project root
2. Check the file contains: `GEMINI_API_KEY=your_key`
3. Ensure no spaces around the `=` sign
4. Restart terminal after creating `.env`

#### Issue 3: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'google.generativeai'
```

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install google-generativeai python-dotenv click radon
```

#### Issue 4: API Rate Limiting

**Error:**
```
Error 429: Resource exhausted
```

**Solution:**
- Wait a few minutes before retrying
- Check your API quota at Google AI Studio
- Reduce batch size when processing multiple files
- Increase `MAX_RETRIES` in `.env`

#### Issue 5: Invalid Syntax in Generated Tests

**Problem:** Generated tests have syntax errors

**Solution:**
1. Run with verbose mode: `smart-test generate file.py -v`
2. Check source file has valid Python syntax
3. Try `--no-ai` flag to generate basic template
4. Report issue with source file example

#### Issue 6: Tests Not Covering Edge Cases

**Problem:** Generated tests are too basic

**Solution:**
- Ensure API key is valid (AI features require API)
- Add docstrings to your functions (helps AI understand intent)
- Use more complex function names (descriptive names help)
- Try `gemini-1.5-pro` model for more sophisticated tests

---

## Best Practices

### 1. Writing Test-Friendly Code

**Good:**
```python
def calculate_discount(price: float, percentage: float) -> float:
    """
    Calculate discount amount.
    
    Args:
        price: Original price
        percentage: Discount percentage (0-100)
    
    Returns:
        Discounted price
    
    Raises:
        ValueError: If percentage is invalid
    """
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100")
    return price * (1 - percentage / 100)
```

**Why it's good:**
- Type hints help generate appropriate test data
- Docstrings provide context for AI
- Clear error handling leads to better error tests

### 2. Organizing Test Files

```
project/
├── src/
│   ├── module1.py
│   ├── module2.py
│   └── utils/
│       └── helpers.py
├── tests/
│   ├── test_module1.py
│   ├── test_module2.py
│   └── utils/
│       └── test_helpers.py
└── .env
```

**Use batch command to maintain structure:**
```bash
smart-test batch src/ -o tests/ -r
```

### 3. Review Generated Tests

**Always review and customize:**
1. ✅ Check test assertions make sense
2. ✅ Add domain-specific test cases
3. ✅ Verify edge cases are covered
4. ✅ Add integration tests if needed
5. ✅ Update fixtures with realistic data

### 4. Iterative Improvement

```bash
# 1. Generate initial tests
smart-test generate mymodule.py

# 2. Run and check coverage
pytest test_mymodule.py --cov=mymodule

# 3. Identify gaps
pytest test_mymodule.py --cov-report=html

# 4. Manually add missing tests

# 5. Regenerate if major refactoring occurs
smart-test generate mymodule.py -o test_mymodule_v2.py
```

### 5. Performance Tips

**For large projects:**
```bash
# Process in smaller batches
smart-test batch src/core/ -o tests/core/
smart-test batch src/utils/ -o tests/utils/
smart-test batch src/api/ -o tests/api/

# Use --no-ai for simple modules
smart-test generate simple_utils.py --no-ai

# Run in parallel (manually)
smart-test generate module1.py &
smart-test generate module2.py &
wait
```

---

## Additional Resources

### Links

- **GitHub Repository**: [https://github.com/Pradyumn-cloud/Verita](https://github.com/Pradyumn-cloud/Verita)
- **Google Gemini API**: [https://ai.google.dev/](https://ai.google.dev/)
- **pytest Documentation**: [https://docs.pytest.org/](https://docs.pytest.org/)
- **unittest Documentation**: [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)

### Further Reading

- Python Testing Best Practices
- Test-Driven Development (TDD)
- Code Coverage Analysis
- Continuous Integration Strategies

---

## Support

For issues, questions, or contributions:

1. **GitHub Issues**: [Create an issue](https://github.com/Pradyumn-cloud/Verita/issues)
2. **Email**: Contact project maintainer
3. **Pull Requests**: Contributions welcome!

---

<div align="center">

**📖 Documentation Version 1.0**

Last Updated: October 2025

Made with ❤️ by Pradyumn

</div>

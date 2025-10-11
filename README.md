<div align="center">

# 🧪 Smart Test Generator

### AI-Powered Python Test Suite Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Powered by Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

**Automatically generate comprehensive, intelligent test files for your Python projects using AI.**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Examples](#-examples)

</div>

---

## 📸 Demo

<!-- Add your screenshot/demo image here -->
![Smart Test Generator Demo](logo.jpg)

---

## 🚀 Features

<table>
<tr>
<td width="50%">

### 🤖 **AI-Powered Intelligence**
Leverages Google Gemini to understand your code's logic, edge cases, and generate meaningful test scenarios

### 🎯 **Smart Code Analysis**
- Complexity analysis
- Function signature detection
- Dependency mapping
- Test coverage recommendations

</td>
<td width="50%">

### 📦 **Batch Processing**
Generate tests for entire projects or directories in one command

### 🔧 **Framework Flexible**
Support for both **pytest** and **unittest** frameworks with proper fixtures and assertions

</td>
</tr>
</table>

### ✨ Additional Features
- 🎨 **Clean CLI Interface** - Simple, intuitive command-line tools
- � **Detailed Documentation** - Generates tests with inline comments
- ⚡ **Fast Processing** - Efficient async API calls
- 🛡️ **Error Handling** - Robust error detection and reporting
- 🔒 **Secure** - Environment-based API key management

---

## 📋 Requirements

- **Python 3.8+**
- **Google Gemini API Key** (Free tier available)
- **pip** package manager

---

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Pradyumn-cloud/Verita.git
cd Verita
```

### 2. Install the Package
```bash
pip install -e .
```

This installs the package in editable mode with all dependencies.

### 3. Set Up API Key

Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

### 4. Verify Installation
```bash
smart-test --help
```

---

## 🎯 Quick Start

### Generate Your First Test

```bash
# Generate test file for a Python module
smart-test generate calculator.py

# Output will be saved as test_calculator.py
```

### Analyze Code Before Testing

```bash
# Get insights about your code
smart-test analyze calculator.py
```

Output shows:
- Complexity score
- Functions detected
- Recommended test strategies
- Test coverage suggestions

### Batch Generate Tests

```bash
# Generate tests for all Python files in a directory
smart-test batch src/ -o tests/
```

---

## 📖 Usage

### Command Overview

```bash
smart-test [COMMAND] [OPTIONS]
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `generate` | Generate test file for a Python source file | `smart-test generate app.py` |
| `analyze` | Analyze code without generating tests | `smart-test analyze app.py` |
| `batch` | Generate tests for all files in a directory | `smart-test batch src/` |

---

## 🔍 Detailed Command Usage

### 1. Generate Command

Generate a comprehensive test file for your Python code:

```bash
# Basic usage
smart-test generate mymodule.py

# Specify output location
smart-test generate mymodule.py -o tests/test_mymodule.py

# Choose unittest framework
smart-test generate mymodule.py -f unittest

# Generate template without AI
smart-test generate mymodule.py --no-ai

# Verbose output
smart-test generate mymodule.py -v
```

**Options:**
- `-o, --output PATH` - Specify custom output file path
- `-f, --framework {pytest|unittest}` - Choose test framework (default: pytest)
- `--no-ai` - Generate basic template without AI analysis
- `-k, --api-key KEY` - Provide API key directly (overrides .env)
- `-v, --verbose` - Enable detailed logging

---

### 2. Analyze Command

Analyze your code structure and get test recommendations:

```bash
smart-test analyze mymodule.py
```

**Output includes:**
- Cyclomatic complexity score
- List of functions and classes
- Recommended test strategies
- Edge cases to consider

---

### 3. Batch Command

Generate tests for multiple files:

```bash
# Process entire directory
smart-test batch src/ -o tests/

# Specific framework for all files
smart-test batch src/ -o tests/ -f unittest

# Verbose batch processing
smart-test batch src/ -o tests/ -v
```

---

## 💡 Examples

### Example 1: Calculator Module

```python
# examples/calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Generate tests:**
```bash
smart-test generate examples/calculator.py
```

**Generated test file includes:**
- ✅ Basic functionality tests
- ✅ Edge case tests (division by zero)
- ✅ Type validation tests
- ✅ Proper fixtures and assertions

---

### Example 2: String Utils Module

```python
# examples/mypackage/string_utils.py
def reverse_string(s):
    return s[::-1]

def is_palindrome(s):
    return s == s[::-1]
```

**Generate with analysis:**
```bash
smart-test analyze examples/mypackage/string_utils.py
smart-test generate examples/mypackage/string_utils.py -o tests/test_string_utils.py
```

---

## 🏗️ Project Structure

```
Verita/
├── smart_test/              # Main package
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── generator.py        # Test generation logic
│   ├── analyzer.py         # Code analysis
│   ├── llm_client.py       # Gemini API client
│   ├── models.py           # Data models
│   ├── config.py           # Configuration
│   └── utils.py            # Utilities
├── examples/               # Example files
│   ├── calculator.py
│   └── mypackage/
├── setup.py               # Package setup
├── .env                   # API key (not tracked)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GEMINI_API_KEY=your_actual_api_key_here

# Optional (with defaults)
GEMINI_MODEL=gemini-1.5-flash
MAX_RETRIES=3
TIMEOUT=30
```

### Custom Configuration

You can override settings via command-line options or modify `smart_test/config.py`.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Pradyumn-cloud/Verita.git
cd Verita

# Install in development mode
pip install -e .

# Run examples
smart-test generate examples/calculator.py
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'smart_test'`
- **Solution:** Run `pip install -e .` in the project root

**Issue:** `API key not found`
- **Solution:** Ensure `.env` file exists with valid `GEMINI_API_KEY`

**Issue:** `Rate limit exceeded`
- **Solution:** Wait a few moments and retry, or check your API quota

**Issue:** Tests not generating
- **Solution:** Run with `-v` flag for verbose output to see error details

---

## 📝 License

This project is licensed under a **Proprietary License**.

**Copyright © 2025 Pradyumn-cloud. All Rights Reserved.**

See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** - For powering the AI test generation
- **Python Community** - For amazing testing frameworks
- **Open Source Contributors** - For inspiration and tools

---

## 📧 Contact

**Author:** Pradyumn  
**GitHub:** [@Pradyumn-cloud](https://github.com/Pradyumn-cloud)  
**Project:** [Verita](https://github.com/Pradyumn-cloud/Verita)

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

Made with ❤️ by Pradyumn

</div>
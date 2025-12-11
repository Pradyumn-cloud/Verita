# GitHub Action Installation Guide

Perfect copy-paste ready examples for using Verita in your GitHub workflows!

## Quick Setup (3 Steps)

### Step 1: Get Your FREE Gemini API Key
Get your key at: https://aistudio.google.com/app/apikey

### Step 2: Add API Key as Repository Secret
1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `GEMINI_API_KEY`
4. Value: Paste your API key
5. Click **Add secret**

### Step 3: Create Workflow File
Create `.github/workflows/smart-test.yml` and copy-paste this:

```yaml
name: Generate Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Allows manual trigger

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate AI Tests
        uses: Pradyumn-cloud/Verita@v4.0.3
        with:
          paths: 'src/'  # Change to your source directory
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          model: 'models/gemini-2.0-flash'  # Fast & recommended
          framework: 'pytest'  # or 'unittest'
          output-dir: 'generated-tests'
      
      - name: Upload Generated Tests
        uses: actions/upload-artifact@v4
        with:
          name: ai-generated-tests
          path: generated-tests/
```

---

## Usage Examples

### Basic Usage - Single Directory
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'src/'
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Multiple Paths - Comma Separated
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'src/,lib/utils.py,app.py'  # Multiple paths
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Single File
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'app.py'  # Single file
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Custom Model (More Powerful)
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'src/'
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
    model: 'models/gemini-pro-latest'  # Most capable
```

### Custom Output & Framework
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'src/'
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
    framework: 'unittest'  # Use unittest instead of pytest
    output-dir: 'tests/ai-generated'  # Custom output directory
```

### Multiple Directories
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'src/,lib/,app/'  # Process multiple directories
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Nested Directories
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'src/models/'  # Recursively processes all .py files
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Mixed Files and Directories
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.3
  with:
    paths: 'app.py,src/models/,lib/utils.py'  # Mix files & directories
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

---

## 🎯 All Supported Scenarios

The action intelligently handles various input patterns:

| Input Type | Example | Result |
|------------|---------|--------|
| Single file | `app.py` | Generates `test_app.py` |
| Directory | `src/` | Tests for all `.py` files in `src/` |
| Multiple files | `app.py,utils.py,config.py` | Generates 3 test files |
| Multiple dirs | `src/,lib/,tests/helpers/` | Processes all directories |
| Nested dir | `src/models/` | Recursively finds all Python files |
| Mixed | `main.py,src/,lib/utils.py` | Handles both files & directories |

**Important Notes:**
- Use **commas without spaces** to separate multiple paths: ✅ `src/,lib/` ❌ `src/, lib/`
- Directory paths are processed recursively (all subdirectories included)
- Only `.py` files are processed; non-Python files are automatically skipped
- Output files are named `test_<original_name>.py`

---

## ⚙️ Configuration Options

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `paths` | Path(s) to scan: directory, file, or comma-separated list | ✅ Yes | - |
| `gemini-api-key` | Your Gemini API key from secrets | ✅ Yes | - |
| `model` | AI model to use (see table below) | ❌ No | `models/gemini-2.0-flash` |
| `framework` | Test framework: `pytest` or `unittest` | ❌ No | `pytest` |
| `output-dir` | Directory for generated test files | ❌ No | `generated-tests` |

---

## 📋 Complete Workflow Examples

### Example 1: Basic - Manual Trigger

Simple workflow for on-demand test generation:

```yaml
name: Generate Tests

on:
  workflow_dispatch:
    inputs:
      paths:
        description: 'Path(s) to scan (e.g., src/ or app.py)'
        required: true
        default: 'src/'

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate AI Tests
        uses: Pradyumn-cloud/Verita@v4.0.3
        with:
          paths: ${{ inputs.paths }}
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
      
      - name: Upload Tests
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: ai-generated-tests
          path: generated-tests/
```

### Example 2: Automatic - On Push

Automatically generate tests when Python files change:

```yaml
name: Auto Generate Tests

on:
  push:
    branches: [ main, develop ]
    paths:
      - '**.py'  # Only run when Python files change

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Tests for All Code
        uses: Pradyumn-cloud/Verita@v4.0.3
        with:
          paths: 'src/,app.py,lib/'  # Cover all your Python code
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          framework: 'pytest'
      
      - name: Upload Tests
        uses: actions/upload-artifact@v4
        with:
          name: generated-tests-${{ github.sha }}
          path: generated-tests/
```

### Example 3: Advanced - With Multiple Options

Full-featured workflow with model selection and custom output:

```yaml
name: AI Test Generation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      paths:
        description: 'Paths to generate tests for'
        required: true
        default: 'src/'
      model:
        description: 'Choose AI model'
        type: choice
        options:
          - models/gemini-2.0-flash
          - models/gemini-2.5-flash
          - models/gemini-pro-latest
        default: models/gemini-2.0-flash
      framework:
        description: 'Testing framework'
        type: choice
        options:
          - pytest
          - unittest
        default: pytest

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
      
      - name: Generate AI-Powered Tests
        uses: Pradyumn-cloud/Verita@v4.0.3
        with:
          paths: ${{ github.event.inputs.paths || 'src/' }}
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          model: ${{ github.event.inputs.model || 'models/gemini-2.0-flash' }}
          framework: ${{ github.event.inputs.framework || 'pytest' }}
          output-dir: 'generated-tests'
      
      - name: Upload Generated Tests
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: ai-generated-tests
          path: generated-tests/
          retention-days: 30
      
      - name: Display Summary
        if: always()
        run: |
          echo "## 🧪 Test Generation Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Configuration:**" >> $GITHUB_STEP_SUMMARY
          echo "- Paths: \`${{ github.event.inputs.paths || 'src/' }}\`" >> $GITHUB_STEP_SUMMARY
          echo "- Model: \`${{ github.event.inputs.model || 'models/gemini-2.0-flash' }}\`" >> $GITHUB_STEP_SUMMARY
          echo "- Framework: \`${{ github.event.inputs.framework || 'pytest' }}\`" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Generated Files:**" >> $GITHUB_STEP_SUMMARY
          ls -lh generated-tests/ 2>/dev/null || echo "No files generated"
```

### Example 4: Test Different Scenarios

Interactive workflow to test various path patterns:

```yaml
name: Test All Scenarios

on:
  workflow_dispatch:
    inputs:
      scenario:
        description: 'Choose test scenario'
        required: true
        type: choice
        options:
          - 'Single file (examples/calculator.py)'
          - 'Single directory (src/)'
          - 'Multiple files (app.py,utils.py)'
          - 'Multiple directories (src/,lib/)'
          - 'Mixed paths (app.py,src/models/)'
          - 'Custom path'
      custom_path:
        description: 'Custom path (if "Custom path" selected)'
        required: false

jobs:
  test-scenario:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set Path Based on Scenario
        id: set-path
        run: |
          case "${{ inputs.scenario }}" in
            "Single file (examples/calculator.py)")
              echo "path=examples/calculator.py" >> $GITHUB_OUTPUT
              ;;
            "Single directory (src/)")
              echo "path=src/" >> $GITHUB_OUTPUT
              ;;
            "Multiple files (app.py,utils.py)")
              echo "path=app.py,utils.py" >> $GITHUB_OUTPUT
              ;;
            "Multiple directories (src/,lib/)")
              echo "path=src/,lib/" >> $GITHUB_OUTPUT
              ;;
            "Mixed paths (app.py,src/models/)")
              echo "path=app.py,src/models/" >> $GITHUB_OUTPUT
              ;;
            "Custom path")
              echo "path=${{ inputs.custom_path }}" >> $GITHUB_OUTPUT
              ;;
          esac
      
      - name: Generate Tests
        uses: Pradyumn-cloud/Verita@v4.0.3
        with:
          paths: ${{ steps.set-path.outputs.path }}
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
      
      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: scenario-test-${{ github.run_number }}
          path: generated-tests/
```

---

## Tips & Best Practices

1. **Start with the default model** (`models/gemini-2.0-flash`) - it's fast and efficient
2. **Use comma-separated paths** to generate tests for multiple specific files
3. **Upload artifacts** so you can review generated tests before committing
4. **Run on pull requests** to automatically generate tests for new code
5. **Set retention days** for artifacts to manage storage costs

---

## Troubleshooting

### Common Issues

**Issue:** Action fails with "API key not found"
- **Solution:** Make sure you created the `GEMINI_API_KEY` secret in repository settings

**Issue:** No tests generated
- **Solution:** Check that your `paths` input points to Python files (`.py`)

**Issue:** Rate limit exceeded
- **Solution:** Wait a few minutes or switch to a less intensive model

---

## More Examples

### Generate Tests on Every Push
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - '**.py'  # Only run when Python files change
```

### Manual Trigger with Custom Options
```yaml
on:
  workflow_dispatch:
    inputs:
      paths:
        description: 'Files/directories to scan'
        required: true
        default: 'src/'
      model:
        description: 'Choose model'
        type: choice
        options:
          - models/gemini-2.0-flash
          - models/gemini-2.5-flash
          - models/gemini-pro-latest
        default: models/gemini-2.0-flash
```

---

## 🔗 Links

- **Repository:** https://github.com/Pradyumn-cloud/Verita
- **Get API Key:** https://aistudio.google.com/app/apikey
- **Issues:** https://github.com/Pradyumn-cloud/Verita/issues

---

Made by Pradyumn

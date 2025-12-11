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
        uses: Pradyumn-cloud/Verita@v4.0.1
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
- uses: Pradyumn-cloud/Verita@v4.0.1
  with:
    paths: 'src/'
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Multiple Paths - Comma Separated
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.1
  with:
    paths: 'src/,lib/utils.py,app.py'  # Multiple paths
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Single File
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.1
  with:
    paths: 'app.py'  # Single file
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Custom Model (More Powerful)
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.1
  with:
    paths: 'src/'
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
    model: 'models/gemini-pro-latest'  # Most capable
```

### Custom Output & Framework
```yaml
- uses: Pradyumn-cloud/Verita@v4.0.1
  with:
    paths: 'src/'
    gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
    framework: 'unittest'  # Use unittest instead of pytest
    output-dir: 'tests/ai-generated'  # Custom output directory
```

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

## Complete Example Workflow

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
        description: 'Model to use'
        required: false
        default: 'models/gemini-2.0-flash'

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
      
      - name: Generate AI-Powered Tests
        uses: Pradyumn-cloud/Verita@v4.0.1
        with:
          paths: ${{ github.event.inputs.paths || 'src/' }}
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          model: ${{ github.event.inputs.model || 'models/gemini-2.0-flash' }}
          framework: 'pytest'
          output-dir: 'generated-tests'
      
      - name: Upload Generated Tests as Artifact
        uses: actions/upload-artifact@v4
        with:
          name: ai-generated-tests
          path: generated-tests/
          retention-days: 30
      
      - name: Display Summary
        run: |
          echo "## Test Generation Complete!" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "Generated tests saved to: \`generated-tests/\`" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Files created:**" >> $GITHUB_STEP_SUMMARY
          ls -la generated-tests/ >> $GITHUB_STEP_SUMMARY
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

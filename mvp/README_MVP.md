# OpenManus MVP - Quick Start Guide

This is the Minimal Viable Product (MVP) version of OpenManus with core functionality only.

## Quick Setup

1. **Install dependencies:**
   ```bash
   python setup_mvp.py
   ```

2. **Configure API key:**
   Edit `config/config.toml` with your LLM provider API key.

3. **Run MVP:**
   ```bash
   # Interactive mode
   python mvp_main.py
   
   # CLI mode
   python mvp_main.py "Calculate the factorial of 5"
   ```

## Core Features

- **Python Execution**: Run Python code safely
- **File Operations**: Create, view, and edit files
- **User Interaction**: Ask for clarification
- **Task Completion**: Signal when done

## Testing

```bash
# Run MVP tests
python -m pytest tests/test_mvp.py -v

# Run specific test
python -m pytest tests/test_mvp.py::TestMVPTools::test_python_execute_basic -v
```

## Example Usage

```bash
python mvp_main.py "Create a Python script that calculates prime numbers up to 100"
```

The MVP agent will:
1. Create the Python script
2. Execute it to verify it works
3. Show you the results
4. Ask if you need any modifications

For full documentation, see [MVP_DOCUMENT.md](MVP_DOCUMENT.md).

# OpenManus MVP (Minimal Viable Product) Documentation

## Overview

This document outlines a Minimal Viable Product (MVP) for OpenManus that provides core AI agent functionality with a reduced codebase suitable for local development and testing. The MVP focuses on essential agent capabilities while removing complex dependencies like browser automation, MCP servers, and advanced visualization tools.

## MVP Scope

### Core Components Included

1. **Basic Agent Framework**
   - `Manus` agent class (simplified)
   - `ToolCallAgent` base class for tool execution
   - Core message handling and memory management

2. **Essential Tools**
   - `PythonExecute` - Execute Python code with timeout safety
   - `StrReplaceEditor` - File viewing, creation, and editing
   - `AskHuman` - Interactive user input capability
   - `Terminate` - Task completion signaling

3. **LLM Integration**
   - Support for OpenAI, Anthropic, and local models (Ollama)
   - Configurable model parameters via TOML configuration

4. **Basic Configuration**
   - TOML-based configuration system
   - LLM provider settings
   - Workspace directory management

### Components Excluded from MVP

- **Browser Automation** (`BrowserUseTool`, `BrowserAgent`)
- **MCP (Model Context Protocol)** servers and clients
- **Advanced Visualization** (VMind/VChart chart generation)
- **Web Search** capabilities (Google, Bing, DuckDuckGo)
- **Docker Sandbox** execution environment
- **Multi-agent Planning** flows
- **AWS Bedrock** integration

## Local Setup Instructions

### Prerequisites

- Python 3.12 or higher
- Git
- API key for at least one LLM provider (OpenAI, Anthropic, or local Ollama)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/twajothi/OpenManus.git
   cd OpenManus
   ```

2. **Create Virtual Environment**
   ```bash
   # Using conda (recommended)
   conda create -n openmanus_mvp python=3.12
   conda activate openmanus_mvp
   
   # OR using venv
   python -m venv openmanus_mvp
   source openmanus_mvp/bin/activate  # On Windows: openmanus_mvp\Scripts\activate
   ```

3. **Install Core Dependencies**
   ```bash
   # Install only essential packages for MVP
   pip install pydantic~=2.10.6 openai~=1.66.3 tenacity~=9.0.0 pyyaml~=6.0.2 loguru~=0.7.3 aiofiles~=24.1.0 colorama~=0.4.6
   ```

4. **Configure LLM Provider**
   ```bash
   # Copy example configuration
   cp config/config.example.toml config/config.toml
   
   # Edit config/config.toml with your API key
   ```

   **For OpenAI:**
   ```toml
   [llm]
   model = "gpt-4o"
   base_url = "https://api.openai.com/v1"
   api_key = "sk-your-api-key-here"
   max_tokens = 4096
   temperature = 0.0
   ```

   **For Anthropic:**
   ```toml
   [llm]
   model = "claude-3-5-sonnet-20241022"
   base_url = "https://api.anthropic.com/v1/"
   api_key = "sk-ant-your-api-key-here"
   max_tokens = 8192
   temperature = 0.0
   ```

   **For Local Ollama:**
   ```toml
   [llm]
   api_type = "ollama"
   model = "llama3.2"
   base_url = "http://localhost:11434/v1"
   api_key = "ollama"
   max_tokens = 4096
   temperature = 0.0
   ```

5. **Create MVP Entry Point**
   
   Create a simplified `mvp_main.py` file:
   ```python
   import asyncio
   from app.agent.manus import Manus
   from app.logger import logger

   async def main():
       # Create simplified Manus agent (MVP version)
       agent = await Manus.create()
       
       try:
           prompt = input("Enter your task: ")
           if not prompt.strip():
               logger.warning("Empty prompt provided.")
               return

           logger.info("Processing your request...")
           await agent.run(prompt)
           logger.info("Task completed.")
       except KeyboardInterrupt:
           logger.warning("Operation interrupted.")
       finally:
           await agent.cleanup()

   if __name__ == "__main__":
       asyncio.run(main())
   ```

### Running the MVP

```bash
# Activate your environment
conda activate openmanus_mvp  # or source openmanus_mvp/bin/activate

# Run the MVP agent
python mvp_main.py
```

## Expected Behavior

### Core Capabilities

1. **Interactive Task Execution**
   - Accept natural language task descriptions
   - Break down tasks into tool-based actions
   - Provide step-by-step execution feedback

2. **Python Code Execution**
   - Execute Python code snippets safely with timeout
   - Handle mathematical calculations, data processing
   - Display output and error messages clearly

3. **File Operations**
   - View file and directory contents
   - Create new files with specified content
   - Edit existing files using string replacement
   - Insert content at specific line numbers
   - Undo recent file modifications

4. **Human Interaction**
   - Ask clarifying questions when needed
   - Request additional information or confirmation
   - Handle user input during task execution

### Example Usage Scenarios

**Scenario 1: Data Analysis Task**
```
User: "Calculate the average of numbers 1 through 100 and save the result to a file"

Expected Agent Actions:
1. Use python_execute to calculate: sum(range(1, 101)) / 100
2. Use str_replace_editor to create a file with the result
3. Confirm completion to user
```

**Scenario 2: File Management Task**
```
User: "Create a Python script that prints 'Hello World' and then run it"

Expected Agent Actions:
1. Use str_replace_editor to create hello.py with print statement
2. Use python_execute to run the script
3. Display the output to user
```

**Scenario 3: Interactive Problem Solving**
```
User: "Help me debug this Python function"

Expected Agent Actions:
1. Use ask_human to request the function code
2. Use python_execute to test the function
3. Use str_replace_editor to create fixed version
4. Explain the issues found and solutions applied
```

### Performance Expectations

- **Response Time**: 2-10 seconds per tool execution
- **Memory Usage**: ~100-500MB depending on task complexity
- **File Size Limits**: Handles files up to several MB efficiently
- **Code Execution**: 5-second timeout for Python execution safety

### Limitations

- No web browsing or internet search capabilities
- No advanced data visualization (charts/graphs)
- No multi-agent coordination
- No persistent memory between sessions
- Limited to local file system operations
- No external API integrations beyond LLM providers

## Architecture Overview

```
MVP OpenManus Architecture:

┌─────────────────┐
│   mvp_main.py   │  ← Entry point
└─────────┬───────┘
          │
┌─────────▼───────┐
│  Manus Agent    │  ← Core agent (simplified)
└─────────┬───────┘
          │
┌─────────▼───────┐
│ ToolCallAgent   │  ← Base tool execution
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Tool Suite    │
├─────────────────┤
│ • PythonExecute │  ← Code execution
│ • StrReplaceEditor │  ← File operations  
│ • AskHuman      │  ← User interaction
│ • Terminate     │  ← Task completion
└─────────────────┘
```

## Development Notes

### Code Modifications for MVP

To create this MVP, the following modifications should be made to the existing codebase:

1. **Simplify Manus Agent**
   - Remove MCP client initialization
   - Remove browser context helper
   - Keep only core tools in available_tools

2. **Create MVP Configuration**
   - Strip down config.toml to essential LLM settings
   - Remove browser, search, sandbox, and MCP configurations

3. **Minimal Dependencies**
   - Install only core packages needed for basic functionality
   - Skip browser automation, visualization, and search dependencies

### Testing the MVP

Basic test scenarios to verify MVP functionality:

```bash
# Test 1: Basic math calculation
python mvp_main.py
> "Calculate 15 * 23 and explain the result"

# Test 2: File creation and editing
python mvp_main.py  
> "Create a file called test.txt with the content 'Hello MVP' and then show me its contents"

# Test 3: Interactive problem solving
python mvp_main.py
> "Help me write a function to find prime numbers"
```

## Future Enhancements

Once the MVP is stable, consider adding:

1. **Web Search** capabilities for information retrieval
2. **Basic Visualization** tools for data analysis
3. **File Upload/Download** functionality
4. **Session Persistence** for continued conversations
5. **Plugin System** for custom tool integration

This MVP provides a solid foundation for understanding OpenManus core concepts while maintaining simplicity for local development and testing.

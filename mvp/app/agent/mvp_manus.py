import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))

from app.agent.toolcall import ToolCallAgent
from app.config import config
from app.tool import ToolCollection, Terminate
from app.tool.python_execute import PythonExecute
from app.tool.str_replace_editor import StrReplaceEditor
from app.tool.ask_human import AskHuman

MVP_SYSTEM_PROMPT = """You are Manus, a helpful AI assistant that can execute Python code, edit files, and interact with users.

You have access to the following tools:
- python_execute: Execute Python code safely with timeout
- str_replace_editor: View, create, and edit files
- ask_human: Ask the user for clarification or additional information
- terminate: Signal task completion

Your workspace directory is: {directory}

Always be helpful, accurate, and explain your actions clearly."""

MVP_NEXT_STEP_PROMPT = "What would you like me to do next?"

class MVPManus(ToolCallAgent):
    """Simplified Manus agent for MVP - core functionality only"""
    
    name: str = "MVPManus"
    description: str = "A simplified AI assistant with core tools for Python execution, file operations, and user interaction"
    
    system_prompt: str = MVP_SYSTEM_PROMPT.format(directory=config.workspace_root)
    next_step_prompt: str = MVP_NEXT_STEP_PROMPT
    
    available_tools: ToolCollection = ToolCollection(
        PythonExecute(),
        StrReplaceEditor(),
        AskHuman(),
        Terminate()
    )
    
    max_observe: int = 5000
    max_steps: int = 20

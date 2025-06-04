import pytest
import pytest_asyncio
import tempfile
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mvp.app.agent.mvp_manus import MVPManus
from app.tool.python_execute import PythonExecute
from app.tool.str_replace_editor import StrReplaceEditor
from app.tool.ask_human import AskHuman
from app.tool.terminate import Terminate

@pytest_asyncio.fixture
async def mvp_agent():
    """Create MVP agent for testing"""
    agent = MVPManus()
    yield agent
    await agent.cleanup()

@pytest.fixture
def temp_workspace():
    """Create temporary workspace for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

class TestMVPTools:
    """Test individual MVP tools"""
    
    @pytest.mark.asyncio
    async def test_python_execute_basic(self):
        """Test basic Python execution"""
        tool = PythonExecute()
        result = await tool.execute(code="print('Hello MVP')")
        assert "Hello MVP" in str(result)
    
    @pytest.mark.asyncio
    async def test_python_execute_math(self):
        """Test mathematical calculations"""
        tool = PythonExecute()
        result = await tool.execute(code="result = 15 * 23\nprint(f'Result: {result}')")
        assert "345" in str(result)
    
    @pytest.mark.asyncio
    async def test_python_execute_error_handling(self):
        """Test Python execution error handling"""
        tool = PythonExecute()
        result = await tool.execute(code="1/0")  # Division by zero
        assert "division by zero" in str(result) or "Error" in str(result)
    
    @pytest.mark.asyncio
    async def test_str_replace_editor_create_file(self, temp_workspace):
        """Test file creation"""
        tool = StrReplaceEditor()
        test_file = temp_workspace / "test.txt"
        
        result = await tool.execute(
            command="create",
            path=str(test_file),
            file_text="Hello MVP World!"
        )
        
        assert test_file.exists()
        assert test_file.read_text() == "Hello MVP World!"
    
    @pytest.mark.asyncio
    async def test_str_replace_editor_view_file(self, temp_workspace):
        """Test file viewing"""
        tool = StrReplaceEditor()
        test_file = temp_workspace / "view_test.txt"
        test_file.write_text("Content to view")
        
        result = await tool.execute(command="view", path=str(test_file))
        assert "Content to view" in str(result)
    
    @pytest.mark.asyncio
    async def test_str_replace_editor_str_replace(self, temp_workspace):
        """Test string replacement in files"""
        tool = StrReplaceEditor()
        test_file = temp_workspace / "replace_test.txt"
        test_file.write_text("Hello World\nThis is a test")
        
        result = await tool.execute(
            command="str_replace",
            path=str(test_file),
            old_str="Hello World",
            new_str="Hello MVP"
        )
        
        assert "Hello MVP" in test_file.read_text()
        assert "Hello World" not in test_file.read_text()
    
    @pytest.mark.asyncio
    async def test_terminate_tool_success(self):
        """Test terminate tool with success status"""
        tool = Terminate()
        result = await tool.execute(status="success")
        assert "success" in str(result)
    
    @pytest.mark.asyncio
    async def test_terminate_tool_failure(self):
        """Test terminate tool with failure status"""
        tool = Terminate()
        result = await tool.execute(status="failure")
        assert "failure" in str(result)

class TestMVPAgent:
    """Test MVP agent functionality"""
    
    @pytest.mark.asyncio
    async def test_agent_creation(self):
        """Test MVP agent can be created"""
        agent = MVPManus()
        assert agent.name == "MVPManus"
        assert len(agent.available_tools.tool_map) == 4  # 4 core tools
        await agent.cleanup()
    
    @pytest.mark.asyncio
    async def test_agent_has_core_tools(self, mvp_agent):
        """Test agent has all required MVP tools"""
        tool_names = set(mvp_agent.available_tools.tool_map.keys())
        expected_tools = {"python_execute", "str_replace_editor", "ask_human", "terminate"}
        assert expected_tools.issubset(tool_names)
    
    @pytest.mark.asyncio
    async def test_agent_properties(self, mvp_agent):
        """Test agent has correct properties"""
        assert mvp_agent.description == "A simplified AI assistant with core tools for Python execution, file operations, and user interaction"
        assert mvp_agent.max_observe == 5000
        assert mvp_agent.max_steps == 20
        assert "workspace" in mvp_agent.system_prompt.lower()
    
    @pytest.mark.asyncio
    async def test_agent_cleanup(self):
        """Test agent cleanup functionality"""
        agent = MVPManus()
        await agent.cleanup()

class TestMVPIntegration:
    """Integration tests for MVP scenarios"""
    
    @pytest.mark.asyncio
    async def test_agent_tool_availability(self, mvp_agent):
        """Test that agent can access all its tools"""
        for tool_name in ["python_execute", "str_replace_editor", "ask_human", "terminate"]:
            assert tool_name in mvp_agent.available_tools.tool_map
            tool = mvp_agent.available_tools.tool_map[tool_name]
            assert hasattr(tool, 'execute')
    
    @pytest.mark.asyncio
    async def test_workspace_directory_exists(self, mvp_agent):
        """Test that workspace directory is properly configured"""
        assert "workspace" in mvp_agent.system_prompt.lower()
        assert "directory" in mvp_agent.system_prompt.lower()

class TestMVPScenarios:
    """Test realistic MVP usage scenarios"""
    
    @pytest.mark.asyncio
    async def test_math_calculation_workflow(self, temp_workspace):
        """Test a complete math calculation workflow"""
        python_tool = PythonExecute()
        file_tool = StrReplaceEditor()
        
        calc_result = await python_tool.execute(code="result = 15 * 23\nprint(f'The result is: {result}')")
        assert "345" in str(calc_result)
        
        result_file = temp_workspace / "calculation_result.txt"
        file_result = await file_tool.execute(
            command="create",
            path=str(result_file),
            file_text="Calculation: 15 * 23 = 345"
        )
        
        assert result_file.exists()
        assert "345" in result_file.read_text()
    
    @pytest.mark.asyncio
    async def test_file_processing_workflow(self, temp_workspace):
        """Test a complete file processing workflow"""
        file_tool = StrReplaceEditor()
        python_tool = PythonExecute()
        
        data_file = temp_workspace / "data.txt"
        await file_tool.execute(
            command="create",
            path=str(data_file),
            file_text="apple\nbanana\ncherry\ndate"
        )
        
        process_code = f"""
with open('{data_file}', 'r') as f:
    lines = f.readlines()
    
processed = [line.strip().upper() for line in lines]
print('Processed items:', processed)
print('Total count:', len(processed))
"""
        
        result = await python_tool.execute(code=process_code)
        assert "APPLE" in str(result)
        assert "Total count: 4" in str(result)

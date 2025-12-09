import pytest
from unittest.mock import patch, MagicMock
from app.workflows.executor import run_workflow

@pytest.mark.asyncio
async def test_run_workflow_execution():
    # We want to test the executor without actually calling OpenAI or reading PDFs
    
    # Mock Tools and Agents
    with patch("app.workflows.executor.TOOLS") as mock_tools, \
         patch("app.workflows.executor.AGENTS") as mock_agents:
        
        # Setup specific tool mocks
        mock_pdf_reader = MagicMock()
        mock_pdf_reader.run.return_value = "Extracted PDF text."
        
        mock_quiz_gen = MagicMock()
        mock_quiz_gen.run.return_value = [{"question": "Q1", "options": ["A","B"], "answer": "A"}]
        
        mock_tools.get.side_effect = lambda name: {
            "pdf_reader": mock_pdf_reader,
            "quiz_generator": mock_quiz_gen
        }.get(name)

        # Setup agent mocks
        mock_tutor = MagicMock()
        mock_tutor.run.return_value = "Summary of the lesson."
        
        mock_agents.get.return_value = mock_tutor
        
        # Define a simple workflow definition for testing
        workflow_def = {
            "id": "test_pipeline",
            "steps": [
                {
                    "id": "extract",
                    "type": "tool",
                    "name": "pdf_reader",
                    "inputs": {"pdf_path": "dummy.pdf"}
                },
                {
                    "id": "summarize",
                    "type": "agent",
                    "name": "tutor_agent",
                    "task": "summarize",
                    "inputs": {"text_content": "{{ steps.extract.output }}"}
                },
                {
                    "id": "quiz",
                    "type": "tool",
                    "name": "quiz_generator",
                    "inputs": {"text_content": "{{ steps.summarize.output }}"}
                }
            ]
        }
        
        inputs = {"lesson_pdf_path": "dummy.pdf"}
        
        result = await run_workflow(workflow_def, inputs)
        
        assert result["workflow_id"] == "test_pipeline"
        assert len(result["steps"]) == 3
        
        # Check outputs were passed correctly via templates
        # 1. Extract
        mock_pdf_reader.run.assert_called()
        assert result["steps"][0].output == "Extracted PDF text."
        
        # 2. Summarize
        # The input to summarize should have been resolved from extract output
        mock_tutor.run.assert_called_with({"text_content": "Extracted PDF text.", "task": "summarize"})
        assert result["steps"][1].output == "Summary of the lesson."
        
        # 3. Quiz
        mock_quiz_gen.run.assert_called_with({"text_content": "Summary of the lesson."})
        assert result["steps"][2].output == [{"question": "Q1", "options": ["A","B"], "answer": "A"}]

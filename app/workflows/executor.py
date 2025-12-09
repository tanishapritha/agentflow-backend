from typing import Dict, Any, List
from app.utils.templating import resolve_template
from app.utils.logger import logger
from app.schemas import WorkflowStepOutput

# Import Tools & Agents
from app.tools.pdf_reader import PDFReaderTool
from app.tools.quiz_generator import QuizGeneratorTool
from app.tools.knowledge_base_writer import KnowledgeBaseWriterTool
from app.agents.tutor_agent import TutorAgent

# Registry of available executables
TOOLS = {
    "pdf_reader": PDFReaderTool(),
    "quiz_generator": QuizGeneratorTool(),
    "knowledge_base_writer": KnowledgeBaseWriterTool()
}

AGENTS = {
    "tutor_agent": TutorAgent()
}

async def run_workflow(workflow_def: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
    steps_output = []
    context = {"inputs": inputs, "steps": {}}
    
    workflow_id = workflow_def.get("id")
    steps = workflow_def.get("steps", [])
    
    final_output_structure = {}

    for step in steps:
        step_id = step["id"]
        step_type = step.get("type", "tool")
        name = step.get("name")
        
        # Resolve Inputs
        step_inputs = step.get("inputs", {})
        resolved_inputs = {}
        for k, v in step_inputs.items():
            resolved_inputs[k] = resolve_template(v, context)
            
        # Execute
        output = None
        status = "success"
        
        try:
            if step_type == "tool":
                tool = TOOLS.get(name)
                if tool:
                    output = tool.run(resolved_inputs)
                else:
                    raise ValueError(f"Tool {name} not found")
            elif step_type == "agent":
                agent = AGENTS.get(name)
                if agent:
                    # Some agents might need 'task' from definition
                    if "task" in step:
                        resolved_inputs["task"] = step["task"]
                    output = agent.run(resolved_inputs)
                else:
                    raise ValueError(f"Agent {name} not found")
            else:
                raise ValueError(f"Unknown step type {step_type}")
                
        except Exception as e:
            logger.error(f"Error in step {step_id}: {e}")
            status = "failed"
            output = str(e)
        
        # Store result
        context["steps"][step_id] = {"output": output}
        
        steps_output.append(WorkflowStepOutput(
            id=step_id,
            status=status,
            output=output
        ))

        # Build final output based on specific steps for the 'lesson' pipeline
        if step_id == "summarize":
            final_output_structure["summary"] = output
        if step_id == "quiz":
            final_output_structure["quiz"] = output

    return {
        "workflow_id": workflow_id,
        "steps": steps_output,
        "final_output": final_output_structure
    }

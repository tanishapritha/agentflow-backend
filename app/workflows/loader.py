import yaml
import os
from typing import List, Dict, Any
from app.schemas import WorkflowMetadata

WORKFLOWS_DIR = os.path.join(os.path.dirname(__file__), "examples")

def list_workflows() -> List[WorkflowMetadata]:
    workflows = []
    if not os.path.exists(WORKFLOWS_DIR):
        return []
        
    for f in os.listdir(WORKFLOWS_DIR):
        if f.endswith(".yaml") or f.endswith(".yml"):
            path = os.path.join(WORKFLOWS_DIR, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                    workflows.append(WorkflowMetadata(
                        id=data.get("id"),
                        name=data.get("name", "Unnamed Workflow")
                    ))
            except Exception as e:
                print(f"Error loading workflow {f}: {e}")
    return workflows

def load_workflow_definition(workflow_id: str) -> Dict[str, Any]:
    for f in os.listdir(WORKFLOWS_DIR):
        if f.endswith(".yaml") or f.endswith(".yml"):
            path = os.path.join(WORKFLOWS_DIR, f)
            with open(path, "r", encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if data.get("id") == workflow_id:
                    return data
    return None

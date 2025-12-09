from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# --- Workflow Discovery ---
class WorkflowMetadata(BaseModel):
    id: str
    name: str

# --- Run Workflow Request ---
class WorkflowRunRequest(BaseModel):
    workflow_id: str
    inputs: Dict[str, Any]

# --- Step Output ---
class WorkflowStepOutput(BaseModel):
    id: str
    status: str
    output: Any

# --- Run Workflow Response ---
class WorkflowRunResponse(BaseModel):
    workflow_id: str
    steps: List[WorkflowStepOutput]
    final_output: Dict[str, Any]

# --- PDF Upload Response ---
class PDFUploadResponse(BaseModel):
    saved_path: str

import shutil
import os
import uuid
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.schemas import (
    WorkflowMetadata, 
    WorkflowRunRequest, 
    WorkflowRunResponse, 
    PDFUploadResponse
)
from app.workflows.loader import list_workflows, load_workflow_definition
from app.workflows.executor import run_workflow
from app.utils.logger import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs"
)

# CORS (Frontend will run on localhost:3000 or similar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AgentFlow Engine is running"}

# 🔵 1. GET /workflows
@app.get("/workflows", response_model=List[WorkflowMetadata])
def get_workflows():
    return list_workflows()

# 🔵 2. POST /run-workflow
@app.post("/run-workflow", response_model=WorkflowRunResponse)
async def run_workflow_endpoint(request: WorkflowRunRequest):
    workflow_def = load_workflow_definition(request.workflow_id)
    if not workflow_def:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    logger.info(f"Running workflow {request.workflow_id} with inputs {request.inputs}")
    
    result = await run_workflow(workflow_def, request.inputs)
    return result

# 🔵 3. POST /upload-pdf
@app.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Save file
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")

    # IMPORTANT: Returning absolute path for local tool usage, 
    # but in Docker this would need to vary. Assuming local run.
    return {"saved_path": file_path}

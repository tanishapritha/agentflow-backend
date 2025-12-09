import io
import pytest
from unittest.mock import patch

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AgentFlow Engine is running"}

def test_get_workflows(client):
    response = client.get("/workflows")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]

def test_upload_pdf(client, tmp_path):
    # Mock file upload
    file_content = b"%PDF-1.4 mock pdf content"
    filename = "test_lesson.pdf"
    
    # Create the 'files' dictionary for the request
    # 'file' is the name of the form field expected by the endpoint
    files = {"file": (filename, io.BytesIO(file_content), "application/pdf")}
    
    # We need to ensure the upload directory exists or is mocked
    # The endpoint uses settings.UPLOAD_DIR.
    # In conftest we haven't strictly patched settings for the app instance unless we use override_settings
    # But for a simple test we can let it write to the temp dir configured in config.py or mock it.
    
    # Let's try mocking shutil.copyfileobj or just let it write (it creates temp dir)
    with patch("shutil.copyfileobj") as mock_copy:
        response = client.post("/upload-pdf", files=files)
        
    # Since we mocked copy, it won't actually write, but the endpoint returns path
    assert response.status_code == 200
    data = response.json()
    assert "saved_path" in data
    assert data["saved_path"].endswith(filename)

def test_upload_invalid_file(client):
    files = {"file": ("test.txt", io.BytesIO(b"text"), "text/plain")}
    response = client.post("/upload-pdf", files=files)
    assert response.status_code == 400

@patch("app.main.run_workflow")
def test_run_workflow_endpoint(mock_run, client):
    # Mock the return value of run_workflow
    mock_run.return_value = {
        "workflow_id": "lesson_auto_pipeline",
        "steps": [],
        "final_output": {}
    }
    
    payload = {
        "workflow_id": "lesson_auto_pipeline",
        "inputs": {"lesson_pdf_path": "/tmp/test.pdf"}
    }
    
    response = client.post("/run-workflow", json=payload)
    if response.status_code != 200:
        print(response.json())
        
    assert response.status_code == 200
    data = response.json()
    assert data["workflow_id"] == "lesson_auto_pipeline"
    mock_run.assert_called_once()

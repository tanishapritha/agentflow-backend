import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_pdf_content():
    return "This is a dummy PDF content for testing purposes. It contains some lesson material."

@pytest.fixture
def mock_env_setup(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("UPLOAD_DIR", "/tmp/test_uploads")

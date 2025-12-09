# AgentFlow Engine - Backend

This project is the backend for the AgentFlow Engine, a workflow automation system used for educational content processing. It exposes a FastAPI service that allows a React frontend to upload PDFs, discover workflows, and execute them logic chains (e.g., PDF -> Summary -> Quiz).

## 📦 API Documentation

### Base URL: `http://127.0.0.1:8000`

### 1. GET /workflows
Returns a list of available workflows.

**Example Response:**
```json
[
  {
    "id": "lesson_auto_pipeline",
    "name": "Lesson → Summary → Quiz"
  }
]
```

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/workflows
```

### 2. POST /run-workflow
Executes a workflow by ID.

**Request Body:**
```json
{
  "workflow_id": "lesson_auto_pipeline",
  "inputs": {
    "lesson_pdf_path": "c:/tmp/uploads/...pdf"
  }
}
```

**Example Response:**
```json
{
  "workflow_id": "lesson_auto_pipeline",
  "steps": [
    { "id": "extract", "status": "success", "output": "..." },
    { "id": "summarize", "status": "success", "output": "..." }
  ],
  "final_output": {
    "summary": "...",
    "quiz": [...]
  }
}
```

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/run-workflow \
     -H "Content-Type: application/json" \
     -d '{"workflow_id": "lesson_auto_pipeline", "inputs": {"lesson_pdf_path": "<PATH>"}}'
```

### 3. POST /upload-pdf
Uploads a PDF file.

**Response:**
```json
{
  "saved_path": "c:\\Users\\tprit\\.agent\\uploads\\..."
}
```

**cURL:**
```bash
curl -F "file=@/path/to/lesson.pdf" http://127.0.0.1:8000/upload-pdf
```

---

## 🚀 How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_key_here
   ```

3. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.
   Docs are at `http://127.0.0.1:8000/docs`.

## 🔗 Connecting Frontend
The React frontend should point its API client to `http://localhost:8000`. Ensure CORS is enabled if they are on different ports (enabled by default in this backend).

from typing import Any, Dict
import pdfplumber
from app.tools.base import BaseTool
from app.utils.logger import logger

class PDFReaderTool(BaseTool):
    name = "pdf_reader"
    description = "Extracts text from a PDF file given its path."

    def run(self, inputs: Dict[str, Any]) -> str:
        pdf_path = inputs.get("pdf_path") or inputs.get("file_path")
        if not pdf_path:
            raise ValueError("PDF Path not provided in inputs")
        
        text_content = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"Failed to read PDF {pdf_path}: {e}")
            return f"Error reading PDF: {e}"

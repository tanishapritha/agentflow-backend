import pytest
from app.utils.templating import resolve_template
from app.workflows.loader import list_workflows, load_workflow_definition
from unittest.mock import MagicMock, patch

def test_resolve_template_basic():
    context = {
        "inputs": {"name": "Alice"},
        "steps": {"step1": {"output": "Hello"}}
    }
    
    # Test simple resolution
    assert resolve_template("{{ inputs.name }}", context) == "Alice"
    assert resolve_template("{{ steps.step1.output }}", context) == "Hello"
    
    # Test no resolution needed
    assert resolve_template("Static text", context) == "Static text"
    
    # Test embedded
    # The current regex might only handle the exact match if it's the whole string or parts.
    # Let's check the implementation of templating.py again. 
    # It uses re.sub, so it should replace occurrences.
    assert resolve_template("Message: {{ inputs.name }}", context) == "Message: Alice"

def test_resolve_template_missing_key():
    context = {"inputs": {}}
    # Should probably leave it or return None/Empty string based on implementation. 
    # Logic in templating.py says: return match.group(0) if error.
    assert resolve_template("{{ inputs.missing }}", context) == "{{ inputs.missing }}"

def test_list_workflows():
    workflows = list_workflows()
    assert isinstance(workflows, list)
    # We created one example workflow
    assert len(workflows) >= 1
    assert workflows[0].id == "lesson_auto_pipeline"

def test_load_workflow_definition():
    wf = load_workflow_definition("lesson_auto_pipeline")
    assert wf is not None
    assert wf["id"] == "lesson_auto_pipeline"
    assert "steps" in wf
    assert len(wf["steps"]) == 3

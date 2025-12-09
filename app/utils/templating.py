import re
from typing import Dict, Any

def resolve_template(template_str: str, context: Dict[str, Any]) -> str:
    """
    Resolves {{ steps.step_id.output }} or {{ inputs.key }} patterns.
    Simple regex-based replacement for this use case.
    """
    if not isinstance(template_str, str):
        return template_str
        
    # Pattern to match {{ variable }}
    pattern = r"\{\{\s*([\w\.]+)\s*\}\}"
    
    def replacer(match):
        path = match.group(1).split(".")
        current = context
        try:
            for key in path:
                current = current[key]
            return str(current)
        except (KeyError, TypeError):
            # If path not found, return original or empty? 
            # Returning original helps debug usually, but let's return original string
            return match.group(0)

    return re.sub(pattern, replacer, template_str)

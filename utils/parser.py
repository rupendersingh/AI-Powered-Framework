import json
from app.llm_client import extract_json
from app.logger import get_logger

logger = get_logger("ai_qa")

def parse_ai_output(raw_output,root_key):
    
    logger.info("Parsing LLM response")
    parsed = extract_json(raw_output)
    
     # Step 2: Ensure top-level is a dictionary
    if not isinstance(parsed,dict):
        raise ValueError("Invalid LLM response: expected JSON object")
        logger.error("JSON request failed")

     # Step 3: Check required key
    if root_key not in parsed:
        raise ValueError(f"Missing {root_key} key in response")
    
    test_scenarios = parsed.get(root_key, [])

    # Step 4: Ensure it's a list
    if not isinstance(test_scenarios, list):
        raise ValueError(f"{root_key}not a list")
        return []
    
    return test_scenarios
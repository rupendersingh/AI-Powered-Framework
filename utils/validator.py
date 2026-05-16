
from app.logger import get_logger

logger = get_logger("ai_qa")

def validate_ai_output(items,required_fields):
    logger.info("Validating and cleaning the output")
    
    cleaned_items = []
    seen_titles = set()
   
    for i, item in enumerate(items):
        #logger.info("for loop started for validator")
        missing_fields = []
        
        if not isinstance(item,dict):
            raise ValueError(f"Data at index {i} is not a dictionary")

        for field in required_fields:
            if field not in item or not item[field]:
                missing_fields.append(field)

        if missing_fields:
            logger.warning(
                f"Scenario Skipped | index={i} | missing_fields={missing_fields}"
            )
            continue
                
            
        title = item.get("title")
        steps = item.get("steps")
        expected_result = item.get("expected_result")
        priority = item.get("priority", "Medium") # Default to Medium if missing
        classification = item.get("classification")

        # Type checks
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Invalid title at index {i}")
        
        if not isinstance(steps, (list, str)) or not steps:
            raise ValueError(f"Steps must be a non-empty list or string at index {i}")

        if isinstance(steps, list):
            if not all(isinstance(step, str) and step.strip() for step in steps):
                raise ValueError(f"Invalid steps content at index {i}")
        elif isinstance(steps, str):
            if not steps.strip():
                raise ValueError(f"Invalid steps content at index {i}")
        
        if not isinstance(expected_result, str) or not expected_result.strip():
            raise ValueError(f"Invalid expected_result at index {i}")

        if not isinstance(priority, str) or not priority.strip():
            raise ValueError(f"Invalid priority at index {i}")

         # --- Cleaning ---
        # Remove extra quotes from title

        title = item.get("title", "").strip().lower()

        if title in seen_titles:
            logger.warning(f"Duplicate item skipped: {title}")
            continue

        seen_titles.add(title)

        # Normalize p
        #priority = priority.capitalize()
        #if priority not in ["High", "Medium", "Low"]:
         #   raise ValueError(f"Invalid priority value at index {i}")

        # Normalize classification
        if not classification:
             raise ValueError(f"Missing classification at index {i}")
             
        classification = classification.capitalize()
        if classification not in ["Positive", "Negative", "Boundary"]:
            raise ValueError(f"Invalid classification value '{classification}' at index {i}")
        
          # Clean steps
        if isinstance(steps, list):
            steps = [step.strip() for step in steps]
        else:
            steps = steps.strip()

        cleaned_items.append(item)

        # Build cleaned scenario
        """cleaned_items.append({
            "title": title,
            "steps": steps,
            "expected_result": expected_result.strip(),
            "priority": priority,
            "scenario_type": scenario_type
        })"""

    return cleaned_items
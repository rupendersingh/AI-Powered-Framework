import json
from app.logger import get_logger
from app.prompts import scenario_generation_prompt
from app.llm_client import extract_json,ask_llm,generate_openrouter_response

logger = get_logger("ai_qa")
REQUIRED_FIELDS = [
    "title",
    "steps",
    "expected_result",
    "priority",
    "scenario_type"
]


def generate_test_scenarios(feature,context):
    

    prompt = scenario_generation_prompt(
        feature,context)

    logger.info("Generating sceanrios....")
    
    try:
        response = generate_openrouter_response(prompt)
        logger.info("Raw response received")
        
        scenarios = parse_scenario_output(response)
        logger.info("Scenarios Extracted")
        # print("\nScenario List\n", scenarios)

        clean_scenarios = validate_scenarios(scenarios)
        logger.info("Scenarios Cleaned")

        return clean_scenarios
    except ValueError as error:
        logger.error(f"Scenario generation failed | error={str(error)}")
        try:
            logger.error(f"Raw response: {response}")
        except:
            pass
        return []

def parse_scenario_output(raw_output):
    
    logger.info("Parsing LLM response")
    parsed = extract_json(raw_output)
    
     # Step 2: Ensure top-level is a dictionary
    if not isinstance(parsed,dict):
        raise ValueError("Invalid LLM response: expected JSON object")
        logger.error("JSON request failed")
    
     # Step 3: Check required key
    if "test_scenarios" not in parsed:
        raise ValueError("Missing 'test_scenarios' key in response")
    
    scenarios = parsed["test_scenarios"]

    # Step 4: Ensure it's a list
    if not isinstance(scenarios, list):
        raise ValueError("'test_scenarios' must be a list")
    
    return scenarios

def validate_scenarios(scenarios):
    logger.info("Validating Scenarios and cleaning scenarios")
    if not isinstance(scenarios, list):
        raise ValueError("Scenarios must be a list")
    
    cleaned_scenarios = []
    missing_fields = []

    for i, scenario in enumerate(scenarios):
        if not isinstance(scenario,dict):
            raise ValueError(f"Scenario at index {i} is not a dictionary")

        for field in REQUIRED_FIELDS:
            if field not in scenario or not scenario[field]:
                missing_fields.append(field)

        if missing_fields:
            logger.warning(
                f"Scenario Skipped | index={index} | missing_fields={missing_fields}"
            )
            continue
                
            
        title = scenario["title"]
        steps = scenario["steps"]
        expected_result = scenario["expected_result"]
        priority = scenario["priority"]
        scenario_type = scenario["scenario_type"]

        # Type checks
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Invalid title at index {i}")
        
        if not isinstance(steps, list) or not steps:
            raise ValueError(f"Steps must be a non-empty list at index {i}")

        if not all(isinstance(step, str) and step.strip() for step in steps):
            raise ValueError(f"Invalid steps content at index {i}")
        
        if not isinstance(expected_result, str) or not expected_result.strip():
            raise ValueError(f"Invalid expected_result at index {i}")

        if not isinstance(priority, str):
            raise ValueError(f"Invalid priority at index {i}")

         # --- Cleaning ---
        # Remove extra quotes from title

        title = title.strip().strip('"')

        # Normalize p
        priority = priority.capitalize()
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError(f"Invalid priority value at index {i}")
        
          # Clean steps
        steps = [step.strip() for step in steps]

        # Build cleaned scenario
        cleaned_scenarios.append({
            "title": title,
            "steps": steps,
            "expected_result": expected_result.strip(),
            "priority": priority,
            "scenario_type": scenario_type
        })

    return cleaned_scenarios

if __name__=="__main__":

    try:
        # Step 1: Collect inputs
        feature = input("\nEnter feature:\n")
        context = input("\nEnter context:\n")
    
        # Step 2: Generate scenarios
        scenarios = generate_test_scenarios(
            feature,
            context,
        )

        # Step 3: Display scenarios
        print("\nGenerated Test Scenarios:\n")

        for index,scenario in enumerate(scenarios, start=1):
            print(f"Scenario {index}")
            print(f"Title: {scenario['title']}")
            print(f"Scenario Type: {scenario['scenario_type']}")
            """print(f"Priority: {scenario['priority']}")
            print(f"Steps:")
            for step in scenario["steps"]:
                print(f" - {step}")
            
            print(f"Expected Result: {scenario['expected_result']}")
            print("-" * 50)"""

        # Step 4: Save to JSON file    
        with open("tests/outputs/test_scenarios.json", "w") as file:
            json.dump(scenarios, file, indent=4)

        print("\nScenarios saved to test_scenarios.json")

    except Exception as e:
           print(f"\nError: {e}")




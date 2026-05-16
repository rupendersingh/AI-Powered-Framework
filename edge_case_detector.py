
import json
from app.logger import get_logger
from app.prompts import edge_case_prompt
from app.llm_client import ask_llm, generate_openrouter_response, extract_json
from utils.parser import parse_ai_output
from utils.validator import validate_ai_output

logger = get_logger("ai_qa")

required_fields = [
    "title",
    "steps",
    "expected_result",
    "priority",
    "classification"
]

def generate_edge_cases(feature, context):

    root_key = "edge_cases"
    prompt = edge_case_prompt(feature,context,"edge_cases")

    logger.info("Generating Edge Case sceanrios....")
    
    try:
        response = generate_openrouter_response(prompt)
        logger.info(f"Raw response received")
        
        raw_scenarios = parse_ai_output(response,root_key)
        logger.info(f"Edge Cases Extracted")
        # print("\nScenario List\n", scenarios)

        clean_scenarios = validate_ai_output(raw_scenarios,required_fields)
        logger.info(f"Edge cases Cleaned")

        return clean_scenarios
    except ValueError as error:
        logger.error(f"Test case generation failed | error={str(error)}")
        try:
            logger.error(f"Raw response: {repr(response)}")
        except:
            pass
        return []

if __name__=="__main__":

    try:
        # Step 1: Collect inputs
        feature = input("\nEnter feature:\n")
        context = input("\nEnter context:\n")
    
        # Step 2: Generate scenarios
        scenarios = generate_edge_cases(
            feature,
            context,
        )

        # Step 3: Display scenarios
        print("\nGenerated Edge Cases:\n")

        for index,scenario in enumerate(scenarios, start=1):
            print(f"Edge Case {index}")
            print(f"Title: {scenario['title']}")
            print(f"Classification: {scenario['classification']}")

        # Step 4: Save to JSON file    
        with open("tests/outputs/edge_cases.json", "w") as file:
            json.dump(scenarios, file, indent=4)

        logger.info("\nScenarios saved to test_scenarios.json")

    except Exception as e:
           logger.error(f"\nError: {e}")
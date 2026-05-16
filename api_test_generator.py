import json
from app.prompts import build_api_test_prompt
from app.logger import get_logger
from app.llm_client import ask_llm, generate_openrouter_response, extract_json
from utils.parser import parse_ai_output
from utils.validator import validate_ai_output

logger = get_logger("api_qa")
required_fields = [
    "title",
    "steps",
    "request_data",
    "expected_status_code",
    "expected_result",
    "classification"
]

def generate_api_test_cases(given_api_details):

    root_key = "api_scenarios"
    
    logger.info("api detials extracted")
    prompt = build_api_test_prompt(given_api_details)
    logger.info("Generating API Scenarios sceanrios....")

    response = generate_openrouter_response(prompt)
    #print("\nRAW RESPONSE:\n", response)
    raw_scenarios = parse_ai_output(response,root_key)
    #print("\nCLEANED RESPONSE:\n", raw_scenarios)

    clean_scenarios = validate_ai_output(raw_scenarios, required_fields)

    return clean_scenarios

def extract_api_details(spec, endpoint, method):
    paths = spec.get("paths", {})
    endpoint_data = paths.get(endpoint)
    if not endpoint_data:
        print(f"Error: Endpoint '{endpoint}' not found in spec.")
        return None

    method_data = endpoint_data.get(method.lower())
    if not method_data:
        print(f"Error: Method '{method}' not found for endpoint '{endpoint}'.")
        return None

    parameters = method_data.get("parameters", [])
    
    request_body = (
        method_data
        .get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
    )
    responses = method_data.get("responses", {})

    api_details = {
        "endpoint": endpoint,
        "method": method.upper(),
        "parameters": parameters,
        "request_body": request_body,
        "responses": responses
    }

    return api_details


sample_spec = {
    "paths": {
        "/login": {
            "post": {
                "parameters": [
                    {
                        "name": "username",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "username": {
                                        "type": "string"
                                    },
                                    "password": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        }
    }
}

api_details = extract_api_details(
    sample_spec,
    "/login",
    "POST"
)

if __name__=="__main__":

    try:
        # Step 2: Generate scenarios
        scenarios = generate_api_test_cases(
            api_details
        )

        # Step 3: Display scenarios
        print("\nGenerated API Scenarios:\n")
        print(scenarios)

        for index,scenario in enumerate(scenarios, start=1):
            print(f"Api Scenario {index}")
            print(f"Title: {scenario['title']}")
            print(f"Classification: {scenario['classification']}")
            

        #Step 4: Save to JSON file    
        with open("tests/outputs/api_cases.json", "w") as file:
            json.dump(scenarios, file, indent=4)

        logger.info("\nScenarios saved to test_scenarios.json")
        

    except Exception as e:
           logger.error(f"\nError: {e}")



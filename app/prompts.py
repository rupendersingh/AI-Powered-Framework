
import json
def _base_instruction():
    return (
        "You must return ONLY valid JSON.\n"
        "Do NOT include explanations, notes, or any text outside JSON.\n"
        "The response must start with '{' and end with '}'.\n"
        "Ensure all keys and strings use double quotes.\n"
        "Ensure JSON is syntactically correct.\n"
        )

def scenario_generation_prompt(feature: str, context: str, root_key: str) -> str:
    return f"""
{_base_instruction()}

You are a Senior QA Engineer designing precise, production-grade test scenarios.

Feature: {feature}
Context: {context}

Return ONLY JSON:

{{
  {root_key}: [
    {{
      "title": "string",
      "steps": ["string"],
      "expected_result": "string",
      "priority": "High/Medium/Low",
      "classification": "Positive/Negative/Boundary"
    }}
  ]
}}

MANDATORY COVERAGE:
- Generate realistic QA scenarios relevant to the provided feature and context.
- Coverage may include validation, edge cases, and security-focused scenarios,
but classification must ONLY be: Positive / Negative / Boundary

STRICT RULES:
- Use precise conditions (e.g., "<8 characters", ">254 length")
- Avoid vague terms like "weak", "invalid", "long"
- Steps must be clear and reproducible (include navigation if needed)
- Include:
  - input validation (format, min/max length, charset)
  - security (SQL injection, XSS, brute force)
  - session handling (valid session, expired session)
  - case sensitivity checks
- Each scenario must be realistic and testable
- No duplicate intent
- Priority:
  - HIGH → core flow + security
  - MEDIUM → validation failures
  - LOW → minor edge cases
- Classification:
  - POSITIVE -> Valid inputs, expected flow
  - NEGATIVE -> Invalid inputs, error handling
  - BOUNDARY -> Edge values, limits
  - Do not generate excessively long sample values.
- Represent boundary values symbolically.

  Example:
  - username length > 254 characters
  - password length < 8 characters

- Do not output massive repeated strings.
  

- Minimum 10 {root_key}
- Output ONLY JSON
"""

def edge_case_prompt(feature: str, context: str, root_key: str) -> str:
    return f"""
{_base_instruction()}

You are a Senior QA Engineer focused on breaking the system using edge cases.

- Generate realistic QA scenarios relevant to the provided feature and context.

Feature: {feature}
Context: {context}

Return ONLY JSON:

{{
  {root_key}: [
    {{
      "title": "string",
      "steps": ["string"],
      "expected_result": "string",
      "priority": "High/Medium/Low",
      "classification": "Positive/Negative/Boundary"

    }}
  ]
}}

STRICT EDGE CASE DEFINITION:
Edge cases are extreme inputs or conditions that can break system behavior — NOT standard validation failures.

MANDATORY COVERAGE:
- Extremely long inputs (e.g., >1000 characters)
- Unicode / emoji input
- Whitespace-only input
- Special characters and injection payloads
- Concurrent requests (parallel execution)
- Encoding anomalies (escaped characters, mixed formats)

STRICT RULES:
- DO NOT include normal validation cases (e.g., invalid email format)
- Each case must attempt to break backend/system behavior
- Expected result must describe system behavior (e.g., rejected before DB, no session created)
- Minimum 8 edge cases
- Do not generate excessively long sample values.
- Represent boundary values symbolically.

  Example:
  - username length > 254 characters
  - password length < 8 characters

- Priority:
  - HIGH → core flow + security
  - MEDIUM → validation failures
  - LOW → minor edge cases
- Classification:
  - POSITIVE -> Valid inputs, expected flow
  - NEGATIVE -> Invalid inputs, error handling
  - BOUNDARY -> Edge values, limits
  - Do not generate excessively long sample values.
- Represent boundary values symbolically.

- Do not output massive repeated strings.
- Output ONLY JSON
"""

def bug_report_prompt(issue_description: str) -> str:
    return f"""
{_base_instruction()}

You are a Senior QA Engineer writing a detailed bug report.

Issue:
{issue_description}

Return ONLY JSON:

{{
  "bug_title": "string",
  "steps_to_reproduce": ["string"],
  "expected_result": "string",
  "actual_result": "string",
  "severity": "Low/Medium/High"
}}

STRICT RULES:
- Steps must be clear and reproducible (include navigation if needed)
- Expected result must describe correct system behavior (e.g., redirect, session creation)
- Actual result must clearly describe observed failure
- Assign severity:
  - HIGH → system failure, core functionality broken, server errors
  - MEDIUM → partial failure or non-critical issue
  - LOW → minor UI issue
- Output ONLY JSON
"""

def build_api_test_prompt(api_details)-> str:
  prompt = f"""
  {_base_instruction()}

  You are a Senior QA api testing expert designing precise and production grade REST API test cases for:

  Endpoint:
  {api_details['endpoint']}

  Method:
  {api_details['method']}

  Parameters:
  {json.dumps(api_details['parameters'], indent=2)}

  Request Body:
  {json.dumps(api_details['request_body'], indent=2)}

  Responses:
  {json.dumps(api_details['responses'], indent=2)}

  Generate:
  - Positive test cases
  - Negative test cases
  - Boundary test cases
  - Authentication test cases
  - Error handling test cases
  - Classification:
    - POSITIVE -> Valid inputs, expected flow
    - NEGATIVE -> Invalid inputs, error handling
    - BOUNDARY -> Edge values, limits
  - Do not add any other classification. Stick to the 3 mentioned above
  - Do not generate excessively long sample values.

  Return ONLY valid JSON.

  Expected JSON format:

  {{
    "api_scenarios": [
      {{
        "title": "",
        "steps": ["string"],
        "classification": "",
        "request_data": {{}},
        "expected_status_code": "",
        "expected_result": ""
      }}
    ]
  }}
  """
  return prompt
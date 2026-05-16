import json
import requests
import re
from app.retry_helper import retry
from app.config import OPENROUTER_API_KEY
from app.logger import get_logger

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

logger = get_logger("ai_qa")

@retry (retries=3,delay=2)
def ask_llm(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "format": "json",   # TRY THIS
        "temperature": 0.2,
        "source": "model",
        "stream": False
    }

    response = requests.post(url, json=payload)
    return response.json()

def parse_json(output):
    try:
        return json.loads(output)
    except Exception:
        return None
    
def validate_response(parsed):
    if "answer" not in parsed:
        return False
    if len(parsed["answer"]) < 5:
        return False
    return True
    
def ask_llm_with_retry(user_input, retries=3):
    prompt = build_prompt(user_input)
    
    for i in range(retries):
        output = ask_llm(prompt)

        try:
            parsed = json.loads(output)

            if validate_schema(parsed):
                return parsed
        except:
            pass

        print(f"Retry {i+1} - invalid format")
    raise Exception("Failed after retries")
    
def validate_schema(data):
    if not isinstance(data, dict):
        return False
    if "answer" not in data or "confidence" not in data:
        return False
    
    if not isinstance(data["confidence"], (int, float)):
        return False
    return True

def build_prompt(user_input):
    return f"""
    You are a strict backend API.

    Return ONLY JSON in EXACT format below.
    DO NOT change keys.

    STRICT FORMAT:
    {{
    "answer": "string OR list",
    "confidence": number
    }}

    Rules:
    - No extra keys
    - No explanation
    - No format deviation
    - If unsure → "answer": "I don't know"

    User Query:
    {user_input}
        """
def repair_json(bad_output):
    return f"""
    Fix this into valid JSON ONLY:

    {bad_output}
    """

def extract_json(response: str):
    """
    Extracts the largest valid JSON object from LLM response.
    Handles greediness and common AI verbosity.
    """
    response = response.strip()
    
    # 1. Try direct parse
    try:
        return json.loads(response)
    except:
        pass

    # 2. Try cleaning markdown markers
    clean_resp = re.sub(r'^```[a-zA-Z]*\n|```$', '', response, flags=re.MULTILINE).strip()
    try:
        return json.loads(clean_resp)
    except:
        pass

    # 3. Iterative search for the largest valid JSON block
    start = response.find('{')
    if start != -1:
        # Try from the end of the string backwards
        for end in range(len(response), start, -1):
            if response[end-1] == '}':
                candidate = response[start:end]
                try:
                    return json.loads(candidate)
                except:
                    # If it looks like truncation, try to repair
                    for closure in ['"', '"}', '"]}', '"}]}', '}', ']}', '}]}', '}]}]}']:
                        try:
                            return json.loads(candidate + closure)
                        except:
                            continue
    
    raise ValueError(f"No valid JSON found. Raw output snippet: {response[:200]}...")


def generate_openrouter_response(prompt: str) -> str:
     
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    api_key = OPENROUTER_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "poolside/laguna-xs.2:free",
        "messages": [{"role": "user","content": prompt}],
        "temperature": 0.2,
    }

    try:
        logger.info("Sending request to OpenRouter")
        
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        logger.info(f"OpenRouter response status: {response.status_code}")
        
        response.raise_for_status()
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        logger.error("OpenRouter request timed out")
        raise
    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Invalid response structure: {str(e)}")
        raise


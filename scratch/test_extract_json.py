
import re
import json

def extract_json(response: str):
    clean_resp = re.sub(r'^```[a-zA-Z]*\n|```$', '', response.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(clean_resp)
    except:
        pass

    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception as e:
            print(f"Regex match failed to parse: {e}")
            print(f"Matched text: {match.group()}")

    return None

# Test case 1: Text around JSON
print("Test 1:", extract_json("Here is JSON: {\"a\": 1} and some text."))

# Test case 2: Multiple blocks (The bug!)
print("Test 2:", extract_json("First: {\"a\": 1} and Second: {\"b\": 2}"))

# Test case 3: Truncated JSON
print("Test 3:", extract_json("{\"api_scenarios\": [{\"title\": \"valid\"}"))

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.llm_client import generate_openrouter_response
from app.prompts import scenario_generation_prompt

prompt = scenario_generation_prompt("Login", "User Authentication")
try:
    response = generate_openrouter_response(prompt)
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write(response)
except Exception as e:
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write("Error: " + str(e))

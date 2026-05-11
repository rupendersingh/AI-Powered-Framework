import json
from app.prompts import (
    edge_case_prompt,
    bug_report_prompt
)


from app.llm_client import ask_llm, extract_json


def run_scenario_test():
    prompt = edge_case_prompt(
        feature="Login System",
        context="user logs in using email and password",
    )

    response = ask_llm(prompt)

    print("\nRAW RESPONSE:\n", response)

    try:
        parsed = extract_json(response)
        print("\nVALID JSON ✅")
        print(json.dumps(parsed, indent=2))
    except Exception as e:
        print("\nINVALID JSON ❌")
        print(e)

def run_bug_report_test():
    prompt = bug_report_prompt(
        issue_description="User enters correct credentials but login fails with 500 error"
    )

    response = ask_llm(prompt)

    print("\nRAW RESPONSE:\n", response)

    try:
        parsed = extract_json(response)
        print("\nVALID JSON ✅")
        print(json.dumps(parsed, indent=2))
    except Exception as e:
        print("\nINVALID JSON ❌")
        print(e)

if __name__=="__main__":
    run_bug_report_test()
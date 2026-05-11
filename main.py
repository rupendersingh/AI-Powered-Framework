from app.llm_client import ask_llm, ask_llm_with_retry

if __name__ == "__main__":
    print(ask_llm_with_retry("Explain API testing"))
    print(ask_llm_with_retry("Give 3 test cases for login"))
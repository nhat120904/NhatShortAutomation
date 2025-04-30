from gpt_utils import llm_completion  # Replace your_module_name with the actual filename (without .py)

def test_llm_completion():
    # Basic inputs
    chat_prompt = "What is the capital of France?"
    system_prompt = "You are a helpful assistant."
    
    try:
        result = llm_completion(chat_prompt=chat_prompt, system=system_prompt, temp=0.5, max_tokens=100)
        print("LLM Response:", result)
    except Exception as e:
        print("Test failed:", str(e))

if __name__ == "__main__":
    test_llm_completion()

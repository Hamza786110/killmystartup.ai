from langchain_ollama import ChatOllama
from startup_state import StartupProfile
from main import results
llm = ChatOllama(model="qwen3:4b")

def analyze_idea(startup_idea: str):
    idea = llm.with_structured_output(StartupProfile)
    return idea.invoke(
        f"Analyze the below startup idea : {startup_idea}"
    )

if __name__ == "__main__":
    from cli_utils import get_startup_idea
 
    startup_idea = get_startup_idea()
    result = analyze_idea(startup_idea)
    print(result)
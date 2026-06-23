from langchain_ollama import ChatOllama
from startup_state import StartupProfile

llm = ChatOllama(model="qwen3:4b")

def analyze_idea(startup_idea: str):
    idea = llm.with_structured_output(StartupProfile)
    return idea.invoke(
        f"Analyze the below startup idea : {startup_idea}"
    )

if __name__ == "__main__":
    result1 = analyze_idea(
        "AI startup that created personalized chatbots for companies"
    )
    print(result1)
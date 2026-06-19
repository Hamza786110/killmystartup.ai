from langchain_ollama import ChatOllama
from startup_state import StartupProfile
llm=ChatOllama(model="qwen3:4b")

model_with_profile=llm.with_structured_output(StartupProfile)
idea_output=model_with_profile.invoke(
    "Analyze the below startup idea - AI startup that created personalized chatbots for companies "
)
print(idea_output)
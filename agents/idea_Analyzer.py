import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from startup_state import StartupProfile
llm=ChatOllama(model="qwen3:4b")

model_with_profile=llm.with_structured_output(StartupProfile)
response=model_with_profile.invoke(
    "Analyze the below startup idea - AI startup that created personalized chatbots for companies "
)
print(response)
import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

llm=ChatOllama(model="qwen3")
question=llm.invoke("what is ai?")
print(question)
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    os.environ["GROQ_API_KEY"] = api_key
llm=ChatGroq(model="qwen/qwen3-32b")


import os
from langchain_groq import chatGroq
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm=chatGroq(model="qwen/qwen3-32b")


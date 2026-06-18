import os
from langchain_google_genai import ChatGoogleGenAI
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm=ChatGoogleGenAI(model="gemini-3.0-flash")

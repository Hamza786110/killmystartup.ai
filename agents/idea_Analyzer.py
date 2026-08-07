from langchain_ollama import ChatOllama
from startup_state import StartupProfile
from typing import cast
import streamlit as st

llm = ChatOllama(model="qwen3:4b")

def analyze_idea(startup_idea: str) -> StartupProfile:
    """Extract a structured StartupProfile from a raw startup idea description."""
    structured_llm = llm.with_structured_output(StartupProfile)
    result = structured_llm.invoke(
        f"Analyze the following startup idea and extract a structured profile:\n\n{startup_idea}"
    )
    return cast(StartupProfile, result)

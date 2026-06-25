import sys
import streamlit as st

def get_startup_idea() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()

    idea = st.text_input("Describe your startup idea:", placeholder="e.g. An AI tool that …")
    if not idea.strip():
        st.info("Please enter a non-empty idea above.")
        st.stop() 
    return idea.strip()
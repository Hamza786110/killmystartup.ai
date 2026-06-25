import sys
import streamlit as st
def get_startup_idea() -> str:
    """
    Get the startup idea from the command line if provided
    otherwise prompt the user to type it in.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()

    st.write("Describe your startup idea:")
    idea = st.text_input("> ").strip()
    while not idea:
        st.write("Please enter a non-empty idea.")
        idea = st.text_input("> ").strip()
    return idea
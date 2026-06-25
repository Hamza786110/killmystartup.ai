import sys
from idea_Analyzer import analyze_idea
from Market_Killer import analyze_market
from Competition_Killer import analyze_competition
from Scoring_Agent import score_startup
import streamlit as st

def get_startup_idea() -> str:
    st.text("Describe your startup idea:")
    idea = st.text_input("> ").strip()
    while not idea:
        st.write("Please enter a non-empty idea.")
        idea = st.text_input("> ").strip()
    return idea


def run_pipeline(startup_idea: str) -> dict:
    """Run all four steps and return every stage's output (not just the final report)."""
    st.write("\nStep 1/4: Analyzing idea...")
    idea_output = analyze_idea(startup_idea)

    st.write("Step 2/4: Analyzing market...")
    market_output = analyze_market(idea_output)

    st.write("Step 3/4: Analyzing competition...")
    competition_output = analyze_competition(idea_output, market_output)

    st.write("Step 4/4: Scoring startup...")
    final_report = score_startup(idea_output, market_output, competition_output)

    return {
        "idea_output": idea_output,
        "market_output": market_output,
        "competition_output": competition_output,
        "final_report": final_report,
    }


def print_results(results: dict) -> None:
    """Print every stage of the pipeline, in order."""
    st.write("\n" + "=" * 70)
    st.write("STARTUP PROFILE")
    st.write("=" * 70)
    for key, value in results["idea_output"].items():
        st.write(f"{key}: {value}")

    st.write("\n" + "=" * 70)
    st.write("MARKET ANALYSIS")
    st.write("=" * 70)
    st.write(results["market_output"]["messages"][-1].content)

    st.write("\n" + "=" * 70)
    st.write("COMPETITION ANALYSIS")
    st.write("=" * 70)
    st.write(results["competition_output"]["messages"][-1].content)

    st.write("\n" + "=" * 70)
    st.write("FINAL VERDICT")
    st.write("=" * 70)
    st.write(results["final_report"])


if __name__ == "__main__":
    startup_idea = get_startup_idea()

    results = run_pipeline(startup_idea)
    if st.success(...):
        st.write(results)
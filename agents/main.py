from idea_Analyzer import analyze_idea
from Market_Killer import analyze_market
from Competition_Killer import analyze_competition
from Scoring_Agent import score_startup
import streamlit as st


if "results" not in st.session_state:
    st.session_state.results = None

st.title("🚀 Startup Killer")
st.write("Enter your startup idea below and let the pipeline tear it apart.")

startup_idea = st.text_input("Describe your startup idea:", placeholder="e.g. An AI tool that …")

if st.button("Analyse"):
    if not startup_idea.strip():

        st.warning("Please enter a non-empty idea.")
    else:
        with st.spinner("Running pipeline…"):
            st.write("Step 1/4: Analysing idea…")
            idea_output = analyze_idea(startup_idea)

            st.write("Step 2/4: Analysing market…")
            market_output = analyze_market(idea_output)

            st.write("Step 3/4: Analysing competition…")
            competition_output = analyze_competition(idea_output, market_output)

            st.write("Step 4/4: Scoring startup…")
            final_report = score_startup(idea_output, market_output, competition_output)

        st.session_state.results = {
            "idea_output": idea_output,
            "market_output": market_output,
            "competition_output": competition_output,
            "final_report": final_report,
        }

# ── render results ────────────────────────────────────────────────────────────
if st.session_state.results:
    results = st.session_state.results

    st.success("Pipeline complete!")

    st.divider()
    st.header("📋 Startup Profile")
    for key, value in results["idea_output"].items():
        st.write(f"**{key}:** {value}")

    st.divider()
    st.header("📈 Market Analysis")
    st.markdown(results["market_output"]["messages"][-1].content)

    st.divider()
    st.header("⚔️ Competition Analysis")
    st.write(results["competition_output"]["messages"][-1].content)

    st.divider()
    st.header("🏁 Final Verdict")
    st.write(results)
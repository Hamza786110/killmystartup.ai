from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from startup_state import CompetitionAnalysis, MarketAnalysis, StartupProfile

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b")
summary_model = ChatOllama(model="deepseek-r1:1.5b", temperature=0)

scoring_agent = create_agent(
    model=model,
    system_prompt="""
You are Scoring Agent, a ruthless startup analyst.

Your mission is to score startup ideas based on market and competition analysis.

You will receive:
- Startup Profile
- Market Analysis
- Competition Analysis

Tasks:
1. Score the startup idea.
2. Provide a final score out of 10.
3. Explain the reasoning.
4. Generate critical questions for the founder.

Output format:

FINAL SCORE: X/10

REASONING:
- ...

QUESTIONS FOR THE FOUNDER:
1. ...
2. ...
3. ...
""",
)


def score_startup(
    idea_output: StartupProfile,
    market_output: MarketAnalysis,
    competition_output: CompetitionAnalysis,
) -> str:
    """Produce the final score, reasoning, and founder questions."""
    competition_summary = summary_model.invoke(
        f"""
Summarize the following competition report in under 250 words:

{competition_output.model_dump_json(indent=2)}
"""
    )
    competition_summary_text = competition_summary.content

    result = scoring_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
        Startup Profile:
        {idea_output.model_dump_json(indent=2)}

        Market Analysis:
        {market_output.model_dump_json(indent=2)}

        Competition Analysis:
        {competition_summary_text}

Provide:
1. Final Startup Score
2. Key Risks
3. Founder Questions
""",
                }
            ]
        }
    )

    return result["messages"][-1].content


if __name__ == "__main__":
    from Competition_Killer import analyze_competition
    from Idea_Analyzer import analyze_idea
    from Market_Killer import analyze_market

    startup_idea = input("Describe your startup idea: ").strip()

    idea_output = analyze_idea(startup_idea)
    market_output = analyze_market(idea_output)
    competition_output = analyze_competition(idea_output, market_output)
    final_report = score_startup(idea_output, market_output, competition_output)

    print("\n===== FINAL VERDICT =====\n")
    print(final_report)
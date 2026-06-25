import os
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
from cli_utils import get_startup_idea
from idea_Analyzer import analyze_idea
from Market_Killer import analyze_market
import streamlit as st

competition_model = ChatOllama(model="deepseek-r1:1.5b")
summary_model = ChatOllama(model="qwen3:4b")

@tool
def search(query: str) -> str:
    """Search the web and return competitor research findings."""

    tavily_key = os.getenv("TAVILY_API_KEY")

    client = TavilyClient(tavily_key)

    response = client.search(
        query=query,
        include_answer="basic",#type:ignore
        search_depth="advanced"
    )

    return response.get("answer", "No answer found")

competition_agent = create_agent(
    model=competition_model,
    tools=[search],
    system_prompt="""
You are Competition Killer, a ruthless startup competitor analyst.

    Your mission is to determine whether existing competitors
    can easily defeat this startup.
    
    You will receive:
    - Startup Profile
    - Market Research
    - Competitor Research
    
    Tasks:
    1. Identify the strongest competitors.
    2. Analyze their strengths, market position, and advantages.
    3. Detect areas where competitors already solve the same problem.
    4. Identify barriers that make it difficult to compete.
    5. Determine whether competitors can easily copy the startup's features.
    6. Generate critical questions for the founder.
    
    Output format:
    
    COMPETITION SCORE: X/10
    
    TOP COMPETITORS:
    - Competitor Name: Reason they are dangerous
    
    COMPETITOR ADVANTAGES:
    - ...
    
    SWITCHING COST RISKS:
    - ...
    
    QUESTIONS FOR THE FOUNDER:
    1. ...
    2. ...
    3. ...
    4. ...
    5. ...
"""
)

summary_agent = create_agent(
    model=summary_model,
    system_prompt="""
    You are a startup analyst.

    Summarize the provided information
    in under 250 words.
    """
)
def create_competition_query(profile):
    industry = profile['Industry'][:80]
    customer = profile['Target_Customer'][:80]
    query = (
        f"Top competitors in {industry} serving {customer}. "
        "Market position, differentiators, funding, competitive advantages."
    )
    return query[:400]

def analyze_competition(idea_output, market_output):
    query = create_competition_query(idea_output)
    research = search.invoke(query)
    idea_summary = summary_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": str(idea_output)
            }
        ]
    })
    market_report = market_output["messages"][-1].content
    market_summary = summary_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": market_report
            }
        ]
    })

    idea_summary_text = idea_summary["messages"][-1].content
    market_summary_text = market_summary["messages"][-1].content

    competition_output = competition_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
            Startup Profile:
            {idea_summary_text}

            Market Summary:
            {market_summary_text}

            Competition Findings:
            {research}

            Based on this research:

            1. Identify the strongest competitors.
            2. Explain why they are dangerous.
            3. Highlight barriers to competition.
            4. Assess whether they can copy the startup.
            5. Ask difficult questions for the founder.
            """
                    }
                ]
            })

    return competition_output

if __name__ == "__main__":
    startup_idea = get_startup_idea()
    idea_output = analyze_idea(startup_idea)
    market_output = analyze_market(idea_output)
    competition_output = analyze_competition(idea_output, market_output)
    st.write(competition_output["messages"][-1].content)
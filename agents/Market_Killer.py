import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from tavily import TavilyClient
from cli_utils import get_startup_idea
from idea_Analyzer import analyze_idea
import streamlit as st
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


@tool
def search(query: str) -> str:
    """Search the web and return market research findings."""
    
    tavily_key = os.getenv("TAVILY_API_KEY")

    client = TavilyClient(tavily_key)

    response = client.search(
        query=query,
        include_answer="basic",#type:ignore
        search_depth="advanced"
    )

    return response.get("answer", "No answer found")


agent = create_agent(
    model=model,
    tools=[search],
    system_prompt="""
    You are Market Killer, a ruthless startup analyst.

    Your mission is to disprove startup ideas using market evidence.
    """
)


def create_market_query(profile):
    industry = profile['Industry'][:50]
    description = profile['Description'][:100]
    customer = profile['Target_Customer'][:50]
    query = (
        f"{industry} {description} for {customer}. "
        "Research competitors, market size, growth trends, barriers to entry."
    )
    return query[:400]


def analyze_market(idea_output):

    query = create_market_query(idea_output)

    research = search.invoke(query)

    market_output = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Startup Profile:
                {idea_output}

                Market Research:
                {research}

                Based on this research,
                identify market risks and ask
                challenging questions.
                """
            }
        ]
    })

    return market_output


if __name__ == "__main__":
    startup_idea = get_startup_idea()
    idea_output = analyze_idea(startup_idea)
    result = analyze_market(idea_output)
    st.markdown(result["messages"][-1].content)

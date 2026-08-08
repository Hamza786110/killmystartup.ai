import os
from typing import cast

from langchain_ollama import ChatOllama
from tavily import TavilyClient

from startup_state import CompetitionAnalysis, MarketAnalysis, StartupProfile

competition_model = ChatOllama(model="deepseek-r1:1.5b")


def _search(query: str) -> str:
    """Search the web and return competitor research findings."""
    tavily_key = os.getenv("TAVILY_API_KEY")
    client = TavilyClient(tavily_key)
    response = client.search(
        query=query,
        include_answer="basic",  # type: ignore
        search_depth="advanced",
    )
    return response.get("answer", "No answer found")


def _create_competition_query(profile: StartupProfile) -> str:
    industry = profile.industry[:80]
    customer = profile.target_customer[:80]
    query = (
        f"Top competitors in {industry} serving {customer}. "
        "Market position, differentiators, funding, competitive advantages."
    )
    return query[:400]


def analyze_competition(
    idea_output: StartupProfile, market_output: MarketAnalysis
) -> CompetitionAnalysis:
    """Run one research call and one structured LLM call to produce a CompetitionAnalysis."""
    query = _create_competition_query(idea_output)
    research = _search(query)

    structured_llm = competition_model.with_structured_output(CompetitionAnalysis)
    result = structured_llm.invoke(
        f"""
        You are Competition Killer, a ruthless startup competitor analyst.
        Determine whether existing competitors can easily defeat this startup.

        Startup Profile:
        {idea_output.model_dump_json(indent=2)}

        Market Summary:
        {market_output.model_dump_json(indent=2)}

        Competition Research:
        {research}

        Identify the strongest competitors, their advantages, switching-cost
        risks, whether they could copy this startup, and ask hard questions
        for the founder.
        """
    )
    return cast(CompetitionAnalysis, result)
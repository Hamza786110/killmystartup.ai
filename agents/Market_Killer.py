import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

from startup_state import MarketAnalysis, StartupProfile

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def _search(query: str) -> str:
    """Search the web and return market research findings."""
    tavily_key = os.getenv("TAVILY_API_KEY")
    client = TavilyClient(tavily_key)
    response = client.search(
        query=query,
        include_answer="basic",  # type: ignore
        search_depth="advanced",
    )
    return response.get("answer", "No answer found")


def _create_market_query(profile: StartupProfile) -> str:
    industry = profile.industry[:50]
    description = profile.description[:100]
    customer = profile.target_customer[:50]
    query = (
        f"{industry} {description} for {customer}. "
        "Research competitors, market size, growth trends, barriers to entry."
    )
    return query[:400]


def analyze_market(idea_output: StartupProfile) -> MarketAnalysis:
    """Run one research call and one structured LLM call to produce a MarketAnalysis."""
    query = _create_market_query(idea_output)
    research = _search(query)

    structured_llm = model.with_structured_output(MarketAnalysis)
    result = structured_llm.invoke(
        f"""
        You are Market Killer, a ruthless startup analyst. Disprove startup
        ideas using market evidence.

        Startup Profile:
        {idea_output.model_dump_json(indent=2)}

        Market Research:
        {research}

        Based on this research, score the market viability, identify market
        risks, and ask challenging questions for the founder.
        """
    )
    return result  # type: ignore[return-value]
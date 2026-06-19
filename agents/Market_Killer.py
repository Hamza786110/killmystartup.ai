import os
from langchain_google_genai import  ChatGoogleGenerativeAI 
from tavily import TavilyClient
from langchain.tools import tool
from langchain.agents import create_agent
from idea_Analyzer import idea_output
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"]=api_key
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
@tool
def search(query:str)->str:
    """Search the web and return market research findings."""
    TAVILY=os.getenv('TAVILY_API_KEY')
    Client=TavilyClient(TAVILY)
    response=Client.search(
        query=query,
        include_answer="basic", # type: ignore
        search_depth="advanced"
    )    
    return response.get("answer","no answer found")
agent=create_agent(
    model=model,
    tools=[search],
    system_prompt=("""
            You are Market Killer, a ruthless startup analyst.

            Your mission is to disprove startup ideas using market evidence.

            You will receive:
            - Startup Profile
            - Market Research

            Tasks:
            1. Find weaknesses in the market.
            2. Identify competitors and market saturation.
            3. Detect unrealistic assumptions.
            4. Highlight reasons customers may not buy.
            5. Explain why the market may be difficult to enter.
            6. Generate critical questions for the founder.

            Output format:

            MARKET SCORE: X/10

            MARKET RISKS:
            - ...

            COMPETITIVE THREATS:
            - ...

            HIDDEN ASSUMPTIONS:
            - ...

            QUESTIONS FOR THE FOUNDER:
            1. ...
            2. ...
            3. ...
                   """
                    )
)

def create_market_query(profile):
    return (
        f"{profile['Industry']} "
        f"AI chatbot personalization platform for "
        f"{profile['Target_Customer']}. "
        "Research competitors, market size, growth trends, "
        "barriers to entry and customer adoption."
    )

query=create_market_query(idea_output)
print(len(query))
if len(query)<=400:
    research=search.invoke(query)
    response2 = agent.invoke({
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

print(response2['messages'][-1].content)

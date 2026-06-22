import os
from langchain_ollama import ChatOllama
from Market_Killer import market_output 
from idea_Analyzer import idea_output
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient

model=ChatOllama(model="deepseek-r1:1.5b")
model2=ChatOllama(model="qwen3:4b")
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


def create_competition_finder(profile):
    return (f"Given the startup profile: {profile['Industry']}, identify the top competitors in the market. "
            "Provide a list of competitors, their market share, and key differentiators. "
            "Focus on companies that directly compete with the startup's product or service. "
            "Include information on recent funding rounds, partnerships, and any competitive advantages they may have. "
            "Output format:\n\n"
    )

query=create_competition_finder(idea_output)
agent=create_agent(
    model=model,
    tools=[search],
    system_prompt="""
    You are Competition Killer, a ruthless startup competitor analyst.
    Your mission is to determine whether existing competitors
    can easily defeat this startup.
    You will receive:
    - Startup Profile
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
    - Competitor Name: Reason they are dangerous
    COMPETITOR ADVANTAGES:
    - ...
    - ...
    SWITCHING COST RISKS:
    - ...
    - ...
    QUESTIONS FOR THE FOUNDER:
    1. ...
    2. ...
    3. ...
    4. ...
    5. ...
    """)

agent2=create_agent(
    model=model2,
    system_prompt="You are a startup analyst. Your task is to summarize the startup profile and market research findings in under 250 words each."
)
market_report=market_output['messages'][-1].content

idea_summary = agent2.invoke(
    {
        "messages":[
            {
                "role":"user",
                "content":f"""
            {idea_output}"""
            }]
})

market_summary = agent2.invoke({
    "messages": [
        {
        "role":"user",
        "content": f""" {market_report}"""
        }]
})

if len(query)<=6000:
    research=search.invoke(query)
    response3 = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
                Startup Profile:
                {idea_summary}

                Market Summary:
                {market_summary}

                 Competition Findings:
                {research}

                 Based on this research,
                search for the top competitors and analyze why they are dangerous to this startup.
                And ask challenging questions.And if competitors are not available through your scope use the search tool to find them and analyze them.
                """
            }
        ]
    })

print(response3['messages'][-1].content)
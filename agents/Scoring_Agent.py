import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv
from Competition_Killer import idea_summary,market_summary,response3,agent2

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
if api_key:
    os.environ["GROQ_API_KEY"]=api_key
model=ChatGroq(model="qwen/qwen3-32b")

agent=create_agent(
    model=model,
    system_prompt=("""
            You are Scoring Agent, a ruthless startup analyst.

            Your mission is to score startup ideas based on market and competition analysis.

            You will receive:
            - Startup Profile
            - Market Research
            - Competitor Research

            Tasks:
            1. Score the startup idea based on market risks and competition.
            2. Provide a final score out of 10.
            3. Generate critical questions for the founder.

            Output format:

            FINAL SCORE: X/10

            QUESTIONS FOR THE FOUNDER:
            1. ...
            2. ...
            3. ...
                   """
                    )
)

competition_summary=agent2.invoke(
    {
        "messages":[
            {
                "role":"user",
                "content":f"""
            {response3}"""
            }]
})



Result=agent.invoke({
    "messages":[
        {
            "role":"user",
            "content":f""" 
            Startup Profile:
            {idea_summary}
            Market Summary:
            {market_summary}
            Competition Findings:
            {competition_summary}
            """
        }
    ]
})

print(Result['messages'][-1].content)
from crewai import Agent, Crew, Process, Task
from tools.analytics import (
    CampaignAnalyticsTool,
    ReportDownloadTool,
    ReportStatusTool,
)
from tools.auth import AuthTool
from tools.campaigns import CampaignsList


auth = AuthTool()
auth_response = auth._run()
token = auth_response["access_token"]


campaign_analyst = Agent(
    role="Campaign Performance Analyst",
    goal="""
        Analyse active lineitems and campaigns. 
        Discover underperforming campaigns and lineitems. 
        Provide recommendations to improve performance.
        """,
    backstory="""
        You're the most experienced online advertising analyst with an indepth backgroud in retail and online advertising.
        You combine various analytical insights to formulate
        strategic campaign performance advice. You are now working for
        a super important customer you need to impress.
        You are passionate about data and  work with leading edge technologies in online industry:
        You have 7 years experience in Data Science or Data Analytics
        Masters degree or higher in a quantitative field (Engineering, Mathematics, Computer Science, Physics, etc.)
        Fluency in the core toolkit of Data Science/Data Analytics, SQL, Python, Spark, etc. 
        Outstanding analytical skills: passion for translating data-speak into relevant, compelling stories
        A background in the digital industry or consulting is a plus
        You have the combination of technical skills, passion for learning, and the soft skills to work with all personality types in a dynamic environment
        You are fluent in English
        """,
    allow_delegation=False,
    cache=True,
    verbose=True,
    max_retry_limit=2,
    tools=[
        CampaignsList(token=token),
        CampaignAnalyticsTool(token=token),
        ReportStatusTool(token=token),
        ReportDownloadTool(token=token),
    ],
)


recomendations = Task(
    description="Ask the user for the account id, example {accountId}. Using the {accountId}, conduct an analysis of the campaigns accessable for this account. Ask the user for the period period of the analysis, example {startDate} and {endDate}. ",
    expected_output="A comprehensive recomendation on hot wo improve the performance the campaigns.",
    agent=campaign_analyst,
    human_input=True,
)


crew = Crew(
    agents=[campaign_analyst],
    tasks=[
        recomendations,
    ],
    process=Process.sequential,
    verbose=True,
    memory=True,
    planning=True,
)

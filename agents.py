from crewai import Agent
from textwrap import dedent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from tools.calculator_tools import CalculatorTools
from tools.auth import AuthTool
from tools.accounts import AccountsTool
from tools.auth import AuthTool

auth = AuthTool()
auth_response = auth._run()
token = auth_response['access_token']


class RetailMediaAgents:
    toker:str
    def __init__(self):
        self.OpenAIGPT4mini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.Ollama = Ollama(model="openhermes")

    def campaigns_agent(self):
        return Agent(
            role="Define agent 1 role here",
            backstory=dedent(f"""Define agent 1 backstory here"""),
            goal=dedent(f"""Define agent 1 goal here"""),
            tools=[AuthTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4mini,
        )
    def lineitems_agent(self):
        return Agent(
            role="Define agent 1 role here",
            backstory=dedent(f"""Define agent 1 backstory here"""),
            goal=dedent(f"""Define agent 1 goal here"""),
            tools=[AuthTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4mini,
        )

    def accounts_agent(self):
        return Agent(
            role="Retail Account Manager",
            backstory=dedent(f"""Define agent 2 backstory here"""),
            goal=dedent(f"""Define agent 2 goal here"""),
            tools=[AuthTool, AccountsTool(token=token)],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4mini,
        )
    def analytics_agent(self):
        return Agent(
            role="Campaign Performance Analyst",
            backstory=dedent(f"""You're the most experienced online advertising analyst with an indepth backgraount in retail and online advertising.
                        You combine various analytical insights to formulate
                        strategic campaign performance advice. You are now working for
                        a super important customer you need to impress."""),
            goal=dedent(f"""Analyse active lineitems and campaigns. 
                        Discover underperforming campaigns and lineitems. 
                        Provide recommendations to improve performance."""),
            tools=[CalculatorTools.calculate],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4mini,
        )
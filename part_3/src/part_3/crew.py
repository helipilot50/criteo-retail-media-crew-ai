import os
from typing import Any
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    FileWriterTool,
    SerperDevTool
)

from part_3.models.account import Account
from part_3.tools.accounts import AccountsTool
from part_3.tools.budget import calculate_monthly_pacing, venue_budget_calculator

from part_3.tools.campaigns import fetch_campaign, new_campaign
from part_3.tools.lineitems import new_auction_lineitem

groq_model = "groq/llama-3.1-70b-versatile"
openai_model = "openai/gpt-4o-mini"
ollama_model = "ollama/llama3.2"

openai_temperature = 0.2


@CrewBase
class Part3Crew:
    """Part 3 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm: LLM = None
    searchTool = SerperDevTool()

    def __init__(self, inputs: dict, account: Account):
        self.artist_name = inputs["artist_name"]
        self.year = inputs["year"]
        self.target_account = account
        self.llm_platform = inputs["target_llm"]
        
        os.makedirs(f"output/{self.llm_platform}", exist_ok=True)

        match inputs["target_llm"]:
            case "groq":
                self.llm = LLM(
                    model=groq_model,
                    temperature=0.1,
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.environ["GROQ_API_KEY"],
                    verbose=True,
                )
                self.summary_llm = LLM(
                    model=groq_model,
                    temperature=0.7,
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.environ["GROQ_API_KEY"],
                    verbose=True,
                )
            case "ollama":
                self.llm = LLM(
                    model=ollama_model,
                    temperature=0.1,
                    api_base="http://localhost:11434",
                    verbose=True,
                )
                self.summary_llm = LLM(
                    model=ollama_model,
                    temperature=0.7,
                    api_base="http://localhost:11434",
                    verbose=True,
                )            
            case "openai":
                self.llm = LLM(
                    model=openai_model,
                    temperature=openai_temperature,
                    api_key=os.environ["OPENAI_API_KEY"],
                    verbose=True,
                )
                self.summary_llm = LLM(
                    model=openai_model,
                    temperature=0.7,
                    api_key=os.environ["OPENAI_API_KEY"],
                    verbose=True,
                )
            case "azure":
                self.llm = LLM(
                    model="azure/" + os.environ["AZURE_OPENAI_DEPLOYMENT"],
                    temperature=openai_temperature,
                    base_url=os.environ["AZURE_API_BASE"],
                    api_key=os.environ["AZURE_API_KEY"],
                    verbose=True,
                )
                self.summary_llm = LLM(
                    model="azure/" + os.environ["AZURE_OPENAI_DEPLOYMENT"],
                    temperature=0.7,
                    base_url=os.environ["AZURE_API_BASE"],
                    api_key=os.environ["AZURE_API_KEY"],
                    verbose=True,
                )

    @agent
    def account_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["account_manager"],
            llm=self.llm,
            vernose=True,
            tools=[AccountsTool()],
        )
    

    @agent
    def campaign_manager(self) -> Agent:
        config = self.agents_config["campaign_manager"]
        return Agent(
            config=config,
            verbose=True,
            llm=self.llm,
            memory=True,
        )

    @agent
    def demographics_agent(self) -> Agent:
        config = self.agents_config["demographics_agent"]
        return Agent(
            config=config,
            verbose=True,
            llm=self.llm,
        )

    @agent
    def concert_venue_agent(self) -> Agent:
        config = self.agents_config["concert_venue_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=self.llm,
    )

    @agent
    def campaign_budget_agent(self) -> Agent:
        config = self.agents_config["campaign_budget_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=self.llm,
        )

    @agent
    def summary_agent(self) -> Agent:
        config = self.agents_config["summary_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=self.summary_llm,
        )

    @agent
    def lineitem_manager(self) -> Agent:
        config = self.agents_config["linitem_manager"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=self.llm,
            memory=True,
        )

    @task
    def research_demographics(self) -> Task:
        return Task(
            config=self.tasks_config["research_demographics"],
            output_file=f"output/{self.llm_platform}/{self.artist_name}_research_demographics.json",
            # parameters={"cats": "cats"},
            agent=self.demographics_agent(),
            async_=True,
        )

    @task
    def find_concert_venues(self) -> Task:
        return Task(
            config=self.tasks_config["find_concert_venues"],
            output_file=f"output/{self.llm_platform}/{self.artist_name}_concert_venues.json",
            # output_json=True,
            agent=self.concert_venue_agent(),
            tools=[self.searchTool],
        )

    @task
    def formulate_lineitem_budget(self) -> Task:
        return Task(
            config=self.tasks_config["formulate_lineitem_budget"],
            output_file=f"output/{self.llm_platform}/{self.artist_name}_venues_budget.json",
            # output_json=True,
            agent=self.campaign_budget_agent(),
            context=[self.find_concert_venues()],
            tools=[venue_budget_calculator],
        )

    @task
    def account(self) -> Task:
        return Task(
            config=self.tasks_config["accounts"],
            output_file=f"output/{self.llm_platform}/{self.artist_name}_accounts.md",
            agent=self.account_manager(),
            verbose=True,
        )

    @task
    def create_campaign(self) -> Task:
        return Task(
            config=self.tasks_config["create_campaign"],
            cache=True,
            output_file=f"output/{self.llm_platform}/{self.artist_name}_campaign.json",
            agent=self.campaign_manager(),
            tools=[
                calculate_monthly_pacing,
                new_campaign,
                fetch_campaign,
            ],
            verbose=True,
        )

    @task
    def create_lineitems(self) -> Task:
        return Task(
            config=self.tasks_config["create_lineitems"],
            cache=True,
            output_file=f"output/{self.llm_platform}/{self.artist_name}_lineitems.json",
            agent=self.lineitem_manager(),
            context=[
                self.find_concert_venues(),
                self.create_campaign(),
                self.formulate_lineitem_budget(),
            ],
            tools=[new_auction_lineitem],
            # human_input=True,
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["summary"],
            output_file=f"output/{self.llm_platform}/{self.artist_name}_summary.md",
            agent=self.summary_agent(),
            context=[
                self.account(),
                self.research_demographics(),
                self.find_concert_venues(),
                self.create_campaign(),
                self.formulate_lineitem_budget(),
                self.create_lineitems(),
            ],
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 3 crew"""
        print("Artist name", self.artist_name)
        print("Year", self.year)
        print("Account Id", self.target_account.id)
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            # process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True,
            # memory=True, #causes weird python error with sqllite.py line 88
            planning=True,
            planning_llm=self.llm,
            output_log_file=f"output/{self.llm_platform}/{self.artist_name}_part_3.log",
            output_file=f"output/{self.llm_platform}/{self.artist_name}_part_3.md",
        )

import os
from typing import Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from part_3.handlers.panel import PanelHandler
from part_3.tools.accounts import AccountsTool
from part_3.tools.campaigns import AccountsCampaignsTool, CampaignTool, NewCampaignTool
from part_3.tools.search import InternetSearch, SearchTools

# only if you use Azure
from langchain_openai import AzureChatOpenAI
from part_3.tools.lineitems import AuctionLineitemsTool, NewAuctionLineitemTool

llm = AzureChatOpenAI(
    model=os.environ["OPENAI_MODEL_NAME"],
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
)
# end Azure


@CrewBase
class Part3Crew:
    """Part 3 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # def __init__(self, instance) -> None:
    #     self.instance = instance

    def __init__(self, inputs: dict) -> Any:
        self.account_id = inputs["account_id"]
        self.artist_name = inputs["artist_name"]
        self.year = inputs["year"]

    @agent
    def campaign_manager(self) -> Agent:
        config = self.agents_config["campaign_manager"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # tools=[
            #     AccountsCampaignsTool(),
            #     CampaignTool(),
            #     NewCampaignTool(),
            #     NewAuctionLineitemTool(),
            #     AuctionLineitemsTool()
            #     ],
            # callbacks=[callback_handler],
            verbose=True,
            llm=llm,
        )

    @agent
    def demographics_agent(self) -> Agent:
        config = self.agents_config["demographics_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=llm,
        )

    @agent
    def concert_venue_agent(self) -> Agent:
        config = self.agents_config["concert_venue_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=llm,
        )

    @agent
    def campaign_budget_agent(self) -> Agent:
        config = self.agents_config["campaign_budget_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=llm,
        )

    @agent
    def summary_agent(self) -> Agent:
        config = self.agents_config["summary_agent"]
        # callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            # callbacks=[callback_handler],
            verbose=True,
            llm=llm,
        )

    @task
    def account(self) -> Task:
        return Task(
            config=self.tasks_config["account"],
            output_file=f"output/{self.artist_name}_account.json",
            agent=self.campaign_manager(),
            tools=[AccountsTool()],
        )

    # @task
    # def ask_for_artist_name(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["ask_for_artist_name"],
    #         output_file="output/artist_name.txt",
    #         agent=self.demographics_agent(),
    #         human_input=True,
    #     )

    @task
    def research_demographics(self) -> Task:
        return Task(
            config=self.tasks_config["research_demographics"],
            output_file=f"output/{self.artist_name}_research_demographics.json",
            parameters={"cats": "cats"},
            agent=self.demographics_agent(),
        )

    @task
    def find_concert_venues(self) -> Task:
        return Task(
            config=self.tasks_config["find_concert_venues"],
            output_file=f"output/{self.artist_name}_concert_venues.json",
            agent=self.concert_venue_agent(),
            tools=[InternetSearch()],
        )

    @task
    def formulate_budget(self) -> Task:
        return Task(
            config=self.tasks_config["formulate_budget"],
            output_file=f"output/{self.artist_name}_budget.json",
            agent=self.campaign_budget_agent(),
            context=[self.research_demographics(), self.find_concert_venues()],
            # human_input=True,
        )

    @task
    def create_campaign(self) -> Task:
        return Task(
            config=self.tasks_config["create_campaign"],
            cache=True,
            output_file=f"output/{self.artist_name}_campaign.json",
            agent=self.campaign_manager(),

            context=[
                self.formulate_budget(),

                self.research_demographics(),
                self.find_concert_venues(),
            ],
            # human_input=True,
        )

    # @task
    # def create_lineitems_for_campaign(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["create_lineitems_for_campaign"],
    #         cache=True,
    #         output_file="output/lineitem_for_campaign.json",
    #         agent=self.campaign_manager(),
    #         context=[self.formulate_budget(), self.ask_for_tour_name(), self.find_concert_venues()],
    #         human_input=True,
    #     )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["summary"],
            output_file=f"output/{self.artist_name}_summary.md",
            agent=self.summary_agent(),
            context=[
                self.account(),
                self.research_demographics(),
                self.find_concert_venues(),
                self.formulate_budget(),
                # self.create_campaign(),
                # self.create_lineitems_for_campaign(),
            ],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 3 crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,  # Azure
            output_log_file="output/part_3.log",
            output_file="output/part_3.md",
        )

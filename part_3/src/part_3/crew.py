import os
from typing import Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from part_3.handlers.panel import PanelHandler
from part_3.tools.analytics import (
    CampaignAnalyticsTool,
    ReportDownloadTool,
    ReportStatusTool,
)
from part_3.tools.campaigns import AccountsCampaignsTool

# only if you use Azure
from langchain_openai import AzureChatOpenAI

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

    def __init__(self, instance) -> None:
        self.instance = instance

    # @agent
    # def campaign_manager(self) -> Agent:
    #     config = self.agents_config["campaign_manager"]
    #     callback_handler = PanelHandler(config["name"], self.instance)
    #     return Agent(
    #         config=config,
    #         tools=[AccountsCampaignsTool()],
    #         callbacks=[callback_handler],
    #         verbose=True,
    #         cache=True,
    #         memory=True,
    #         llm=llm,
    #     )

    @agent
    def demographics_agent(self) -> Agent:
        config = self.agents_config["demographics_agent"]
        callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            callbacks=[callback_handler],
            verbose=True,
            cache=True,
            memory=True,
            llm=llm,
        )

    @agent
    def concert_venue_agent(self) -> Agent:
        config = self.agents_config["concert_venue_agent"]
        return Agent(
            config=config,
            verbose=True,
            cache=True,
            memory=True,
            llm=llm,
        )

    @task
    def ask_for_tour_name(self) -> Task:
        return Task(
            config=self.tasks_config["ask_for_tour_name"],
            cache=True,
            output_file="output/artist_name.txt",
            agent=self.demographics_agent(),
            human_input=True,
        )

    @task
    def research_demographics(self) -> Task:
        return Task(
            config=self.tasks_config["research_demographics"],
            cache=True,
            output_file="output/research_demographics.json",
            parameters={"cats": "cats"},
            agent=self.demographics_agent(),
        )

    @task
    def find_concert_venues(self) -> Task:
        return Task(
            config=self.tasks_config["find_concert_venues"],
            cache=True,
            output_file="output/concert_venues.json",
            agent=self.concert_venue_agent(),
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

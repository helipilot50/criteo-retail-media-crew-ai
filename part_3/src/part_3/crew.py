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

    @agent
    def campaign_manager(self) -> Agent:
        config=self.agents_config["campaign_manager"]
        callback_handler = PanelHandler(config["name"], self.instance)
        return Agent(
            config=config,
            tools=[AccountsCampaignsTool()],
            callbacks=[callback_handler],
            verbose=True,
            cache=True,
            memory=True,
            llm=llm,
        )


    @task
    def campaigns(self) -> Task:
        return Task(
            config=self.tasks_config["campaigns"],
            cache=True,
            output_file="output/campaign_ids.json",
            agent=self.campaign_manager(),
            human_input=True,
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
            planning_llm=llm,  # Azurepanel serve app.pypanel serve app.py
            output_log_file="output/part_3.log",
            output_file="output/part_3.md",
        )

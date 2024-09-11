from datetime import date, datetime
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    FileWriterTool,
    FileReadTool,
    DirectoryReadTool,
    DirectorySearchTool,
)

from pydantic import BaseModel, Field
from typing import List, Optional

from part_2.tools.charts import BarChartTool, PieChartTool
from part_2.tools.campaigns import CampaignsTool

# only if you use Azure
from langchain.chat_models.azure_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    model=os.environ["OPENAI_MODEL_NAME"],
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
)
# end Azure


class Campaign(BaseModel):
    """Campaign model"""

    id: str = Field(..., description="ID of the campaign")
    name: str = Field(..., description="Name of the campaign")
    budget: float = Field(..., description="Budget of the campaign")
    budgetSpent: float = Field(..., description="Budget spent of the campaign")
    startDate: str = Field(..., description="Start date of the campaign")
    status: str = Field(..., description="Status of the campaign")
    type: str = Field(..., description="Type of the campaign")


class CampaignList(BaseModel):
    campaigns: List[Campaign] = Field(..., description="Campaigns collection")
    totalItems: int = Field(..., description="Total items in the collection")


@CrewBase
class Part2Crew:
    """Part2 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def campaign_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_reader"],
            tools=[CampaignsTool()],
            # Azure
            llm=llm,
        )

    @agent
    def visualizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["visualizer_agent"],
            tools=[PieChartTool(), BarChartTool()],
            # Azure
            llm=llm,
        )

    @agent
    def campaign_reporter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_reporter_agent"],
            tools=[DirectoryReadTool(), FileReadTool()],
            # Azure
            llm=llm,
        )

    @task
    def fetch_campaigns_task(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_campaigns_with_budget_task"],
            output_file="output/campaigns_with_budget.json",
            tools=[
                CampaignsTool(),
            ],
            agent=self.campaign_reader(),
            output_json=CampaignList,
        )

    @task
    def campaigns_budget_pie_chart(self) -> Task:
        return Task(
            config=self.tasks_config["campaigns_budget_pie_chart"],
            tools=[
                PieChartTool(),
            ],
            agent=self.visualizer_agent(),
            context=[self.fetch_campaigns_task()],
        )

    @task
    def campaigns_report(self) -> Task:
        return Task(
            config=self.tasks_config["campaigns_report"],
            output_file="output/campaigns_report.md",
            agent=self.campaign_reporter_agent(),
            asynch=True,
            context=[
                self.fetch_campaigns_task(),
                self.campaigns_budget_pie_chart(),
            ],  # context improves consistency
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 2 crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,  # Azure
            output_log_file="output/part_2.log",
        )

import os
from datetime import date, datetime
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
)
from pydantic import BaseModel, Field
from typing import List, Optional

from part_2.tools.charts import BarChartTool, PieChartTool
from part_2.tools.campaigns import CampaignsTool

# only if you use Azure
# from langchain_openai import AzureChatOpenAI

# llm = AzureChatOpenAI(
#     model=os.environ["OPENAI_MODEL_NAME"],
#     deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
# )
# end Azure

# only if you use Groq
from langchain_groq import ChatGroq

llm = ChatGroq(
    model=os.environ["GROQ_AI_MODEL_NAME"],
    api_key=os.environ["GROQ_API_KEY"],
    verbose=True,
)

# end Groq


class Campaign(BaseModel):
    """Campaign model"""

    id: str = Field(..., description="ID of the campaign")
    name: str = Field(..., description="Name of the campaign")
    budget: float = Field(..., description="Budget of the campaign")
    budgetSpent: float = Field(..., description="Budget spent of the campaign")
    startDate: str = Field(..., description="Start date of the campaign")
    # endDate: str = Optional(Field(..., description="Start date of the campaign"))
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
    def campaign_manager(self) -> Agent:
        config = self.agents_config["campaign_manager"]
        return Agent(
            config=config,
            llm=llm, # Azure or Groq
        )

    @agent
    def visualizer_agent(self) -> Agent:
        config = self.agents_config["visualizer_agent"]
        return Agent(
            config=config,
            tools=[PieChartTool(), BarChartTool()],
            llm=llm, # Azure or Groq
        )

    @agent
    def campaign_reporter_agent(self) -> Agent:
        config = self.agents_config["campaign_reporter_agent"]
        return Agent(
            config=config,
            tools=[DirectoryReadTool(), FileReadTool()],
            llm=llm, # Azure or Groq
        )

    @task
    def fetch_campaigns_task(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_campaigns_task"],
            output_file="output/campaigns.json",
            tools=[
                CampaignsTool(),
            ],
            agent=self.campaign_manager(),
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
            context=[self.fetch_campaigns_task()], # context improves consistency
        )

    @task
    def campaigns_report(self) -> Task:
        return Task(
            config=self.tasks_config["campaigns_report"],
            output_file="output/campaigns_report.md",
            agent=self.campaign_reporter_agent(),
            asynch=True,
            context=[ # context improves consistency
                self.fetch_campaigns_task(),
                self.campaigns_budget_pie_chart(),
            ],  
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
            planning_llm=llm,
            output_log_file="output/part_2.log",
        )

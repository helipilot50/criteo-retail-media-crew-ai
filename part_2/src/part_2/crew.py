from datetime import date, datetime
import os
from part_2.tools.charts import BarChartTool, PieChartTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from part_2.tools.campaigns import CampaignsTool
from part_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool
from pydantic import BaseModel, Field
from typing import List

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


class CampaignList(BaseModel):
    campaigns: List[Campaign] = Field(..., description="List of campaigns")


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
            tools=[
                PieChartTool(),
            ],
            # Azure
            llm=llm,
        )

    @task
    def fetch_campaigns_task(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_campaigns_task"],
            output_file="output/campaigns.json",
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
            asynch=True,
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

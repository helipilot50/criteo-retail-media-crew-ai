from datetime import date, datetime
import os
from part_2.tools.charts import BarChartTool
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
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"]
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

class Lineitem(BaseModel):
    """Lineitem model"""
    id: str = Field(..., description="ID of the Lineitem")
    campaignId: str = Field(..., description="ID of the campaign ownin this Lineitem")
    startDate: date = Field(..., description="Start date of the Lineitem")
    name: str = Field(..., description="Name of the Lineitem")
    budget: float = Field(..., description="Budget of the Lineitem")
    status: str = Field(..., description="Status of the Lineitem")
    createdAt: datetime = Field(..., description="Creation date of the Lineitem")
    
class LineitemList(BaseModel):
    lineitems: List[Lineitem] = Field(..., description="List of Lineitems")

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
    def lineitems_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["lineitems_reader"],
            tools=[
                AuctionLineitemsTool(),
            ],
            # Azure
            llm=llm,
        )

    @agent
    def lineitem_reducer(self) -> Agent:
        return Agent(
            config=self.agents_config["lineitem_reducer"],
            # Azure
            llm=llm,
        )

    @agent
    def visualizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["visualizer_agent"],
            tools=[
                BarChartTool(),
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
    def fetch_auction_lineitems(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_auction_lineitems"],
            output_file="output/campaigns_auction_lineitems.json",
            tools=[
                AuctionLineitemsTool(),
            ],
            agent=self.lineitems_reader(),
            output_json=LineitemList,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 2 crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,  # Azure
            output_log_file="output/part_2.log",
        )

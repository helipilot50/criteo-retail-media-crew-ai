import os
from part_2.tools.charts import BarChartTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from part_2.tools.campaigns import CampaignsTool
from part_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool


# only if you use Azure
from langchain.chat_models.azure_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    model="gpt-4o", deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"]
)

# end Azure


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

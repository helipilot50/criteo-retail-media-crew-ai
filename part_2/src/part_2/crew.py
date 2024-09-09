from part_2.tools.charts import BarChartTool, PieChartTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from part_2.tools.accounts import AccountsTool
from part_2.tools.campaigns import CampaignsTool
from part_2.tools.lineitems import AuctionLineitemsTool, PreferredLineitemsTool
from crewai_tools import FileWriterTool, FileReadTool, DirectoryReadTool, DirectorySearchTool


@CrewBase
class Part2Crew:
    """Part2 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def campaign_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_reader"],
            tools=[
                CampaignsTool()
            ],
        )
    
    @agent
    def lineitems_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["lineitems_reader"],
            tools=[
                AuctionLineitemsTool(),
            ],
        )

    @agent
    def lineitem_reducer(self) -> Agent:
        return Agent(
            config=self.agents_config["lineitem_reducer"],
        )
    
    @agent
    def visualizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["visualizer_agent"],
            tools=[
                BarChartTool(),
            ],
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
    
    # @task
    # def sumarise_monthly_lineitem_budget(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["sumarise_monthly_lineitem_budget"],
    #         output_file="output/monthly_lineitem_budget.json",
    #         agent=self.lineitem_reducer(),
    #     )

    # @task
    # def lineitems_budget_chart(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["lineitems_budget_chart"],
    #         tools=[
    #             BarChartTool(),
    #         ],
    #         agent=self.visualizer_agent(),
        # )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 2 crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=True,
            planning_llm=ChatOpenAI(model="gpt-4o-mini"),
            output_log_file="output/part_2.log",
        )

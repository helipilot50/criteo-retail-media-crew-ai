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

    # @agent
    # def account_manager(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["account_manager"],
    #         tools=[
    #             AccountsTool(),
    #         ],
    #     )

    @agent
    def campaign_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_manager"],
            tools=[
                CampaignsTool()
            ],
        )
    
    @agent
    def lineitems_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["lineitems_manager"],
            tools=[
                AuctionLineitemsTool(),
                # PreferredLineitemsTool(),
            ],
        )

    # @agent
    # def analyst(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["analyst"],
    #         tools=[BarChartTool()],
    #     )
    

    @task
    def campaigns(self) -> Task:
        return Task(
            config=self.tasks_config["campaigns_task"],
            output_file="output/campaigns.json",
        )
    

    # @task
    # def preferred_lineitems(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["preferred_lineitems"],
    #     )
    
    @task
    def auction_lineitems(self) -> Task:
        return Task(
            config=self.tasks_config["auction_lineitems"],
            output_file="output/campaigns_auction_lineitems.json",
        )

    # @task
    # def lineitems_budget_chart(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["lineitems_budget_chart"],
    #     )

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

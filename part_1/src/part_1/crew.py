from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from part_1.tools.auth import AuthTool
from part_1.tools.accounts import AccountsTool, RetailersTool, BrandsTool

auth = AuthTool()
auth_response = auth._run()
token = auth_response["access_token"]


@CrewBase
class Part1Crew:
    """Part 1 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def account_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["account_manager"],
            tools=[
                AccountsTool(token=token),
                RetailersTool(token=token),
                BrandsTool(token=token),
            ],
        )

    @task
    def accounts(self) -> Task:
        return Task(
            config=self.tasks_config["accounts"], 
            output_file="output/accounts.md"
        )

    @task
    def brands(self) -> Task:
        return Task(
            config=self.tasks_config["brands"],
            output_file="output/brands.md",
        )

    @task
    def retailers(self) -> Task:
        return Task(
            config=self.tasks_config["retailers"],
            output_file="output/retailers.md",
        )

    @task
    def analytics(self) -> Task:
        return Task(
            config=self.tasks_config["analytics"],
            output_file="output/analytics.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 1 crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=ChatOpenAI(model="gpt-4o-mini"),
            output_log_file="output/part_1.log",
        )

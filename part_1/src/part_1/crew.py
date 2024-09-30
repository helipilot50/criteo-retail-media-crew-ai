import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from part_1.tools.accounts import AccountsTool, RetailersTool, BrandsTool

# only if you use Azure
# from langchain_openai import AzureChatOpenAI

# llm = AzureChatOpenAI(
#     model=os.environ["OPENAI_MODEL_NAME"],
#     deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
# )
# end Azure

# only if you use Groq
from crewai import LLM

llm = LLM(
    model=os.environ["GROQ_AI_MODEL_NAME"],
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
# end Groq


@CrewBase
class Part1Crew:
    """Part 1 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    """
    Account manager agent instance created from the config file.
    The function is decorated with the @agent decorator to indicate that it is an agent.
    """

    @agent
    def account_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["account_manager"],
            llm=llm,  # Azure or Groq
            max_iter=1,
        )

    """
    Accounts task instance created from the config file.
    This function is decorated with the @agent decorator to indicate that it is an agent.
    It's job is to retrive Accounts data and produce a Markdown file.
    """

    @task
    def accounts(self) -> Task:
        return Task(
            config=self.tasks_config["accounts"],
            output_file="output/accounts.md",
            tools=[
                AccountsTool(),
            ],
        )

    """
    Brands task instance created from the config file.
    This function is decorated with the @agent decorator to indicate that it is an agent.
    It's job is to retrive Brands data for a specific Account and produce a Markdown file.
    """

    @task
    def brands(self) -> Task:
        return Task(
            config=self.tasks_config["brands"],
            output_file="output/brands.md",
            asynch=True,
            context=[self.accounts()],
            tools=[
                BrandsTool(),
            ],
        )

    """
    Retailers task instance created from the config file.
    This function is decorated with the @agent decorator to indicate that it is an agent.
    It's job is to retrive Retailers data for a specific Account and produce a Markdown file.
    """

    @task
    def retailers(self) -> Task:
        return Task(
            config=self.tasks_config["retailers"],
            output_file="output/retailers.md",
            asynch=True,
            context=[self.accounts()],
            tools=[
                RetailersTool(),
            ],
        )

    """
    This function creates  the crew! It is decorated with the @crew decorator to indicate that it is a crew.
    The crew orchestrates the agents and tasks to complete the process.
    """

    @crew
    def crew(self) -> Crew:
        """Creates the Part 1 crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_log_file="output/part_1.log",
        )

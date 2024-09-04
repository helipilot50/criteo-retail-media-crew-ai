from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from part_1.tools.auth import AuthTool
from part_1.tools.accounts import AccountsTool, RetailersTool, BrandsTool

import os

# For local testing using ollama. WARNING: Unless you have a powerful GPU, this will be VERY VERY slow.
# os.environ["OPENAI_API_KE"]='NA' # No API Key required for Ollama
# ollm = ChatOllama(
#     model = "llama3.1",
#     base_url = "http://localhost:11434")

auth = AuthTool()
auth_response = auth._run()
token = auth_response["access_token"]


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
            tools=[
                AccountsTool(token=token),
                RetailersTool(token=token),
                BrandsTool(token=token),
            ],
            # For local testing using ollama"
            # llm=ollm
        )

    """
    Accounts task instance created from the config file.
    This function is decorated with the @agent decorator to indicate that it is an agent.
    It's job is to retrive Accounts data and produce a Markdown file.
    """
    @task
    def accounts(self) -> Task:
        return Task(
            config=self.tasks_config["accounts"], output_file="output/accounts.md",
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
            memory=True,
            planning=True,
            # For local testing using ollama"
            #planning_llm=ollm,
            planning_llm=ChatOpenAI(model="gpt-4o-mini"),
            output_log_file="output/part_1.log",
        )

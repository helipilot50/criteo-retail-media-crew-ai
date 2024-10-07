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
			model="groq/llama-3.1-8b-instant",
			temperature=0.7,
			base_url="https://api.groq.com/openai/v1",
			api_key=os.environ["GROQ_API_KEY"],
		)

# end Groq


@CrewBase
class Part1Crew:
    """Part 1 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

 

    @agent
    def account_manager(self) -> Agent:
        """
        Account manager agent instance created from the config file.
        The function is decorated with the @agent decorator to indicate that it is an agent.
        """
        return Agent(
            config=self.agents_config["account_manager"],
            llm=llm,  # Azure or Groq
            max_iter=1,
        )



    @task
    def accounts(self) -> Task:
        """
        Accounts task instance created from the config file.
        This function is decorated with the @agent decorator to indicate that it is an agent.
        It's job is to retrieve Accounts data and produce a Markdown file.
        """
        return Task(
            config=self.tasks_config["accounts"],
            output_file="output/accounts.md",
            tools=[
                AccountsTool(),
            ],
        )



    @task
    def brands(self) -> Task:
            """
            Brands task instance created from the config file.
            This function is decorated with the @agent decorator to indicate that it is an agent.
            It's job is to retrieve Brands data for a specific Account and produce a Markdown file.
            """     
            return Task(
            config=self.tasks_config["brands"],
            output_file="output/brands.md",
            asynch=True,
            context=[self.accounts()],
            tools=[
                BrandsTool(),
            ],
        )



    @task
    def retailers(self) -> Task:
            """
            Retailers task instance created from the config file.
            This function is decorated with the @agent decorator to indicate that it is an agent.
            It's job is to retrieve Retailers data for a specific Account and produce a Markdown file.
            """       
            return Task(
            config=self.tasks_config["retailers"],
            output_file="output/retailers.md",
            asynch=True,
            context=[self.accounts()],
            tools=[
                RetailersTool(),
            ],
        )



    @crew
    def crew(self) -> Crew:
        """
        This function creates  the crew! It is decorated with the @crew decorator to indicate that it is a crew.
        The crew orchestrates the agents and tasks to complete the process.
        """        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            planning=True,
            planning_llm=llm,  
            verbose=True,
            output_log_file="output/part_1.log",
        )

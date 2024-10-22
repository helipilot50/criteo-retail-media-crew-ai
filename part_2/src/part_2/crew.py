import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    FileReadTool,
)

from part_2.models.campaign import CampaignList
from part_2.tools.calculator_tools import SumListTool
from part_2.tools.charts import BarChartTool, PieChartTool
from part_2.tools.campaigns import AccountCampaignsTool

groq_model = "groq/llama-3.1-70b-versatile"
openai_model = "openai/" + os.environ["OPENAI_MODEL_NAME"]


@CrewBase
class Part2Crew:
    """Part2 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm: LLM = None

    def __init__(self, inputs: dict):
        """
        Initializes the Crew class with an instance of the LLM model.
        Attributes:
            llm (LLM): An instance of the LLM class initialized with specific parameters.
                - model (str): The model identifier, set to "groq/llama-3.1-8b-instant".
                - temperature (float): The temperature setting for the model, set to 0.7.
                - base_url (str): The base URL for the API, set to "https://api.groq.com/openai/v1".
                - api_key (str): The API key for authentication, retrieved from the environment variable "GROQ_API_KEY".
        """
        match inputs["target_llm"]:
            case "groq":
                self.llm = LLM(
                    model=groq_model,
                    temperature=0.1,
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.environ["GROQ_API_KEY"],
                    verbose=True,
                )
                self.reporter_llm = LLM(
                    model=groq_model,
                    temperature=0.7,
                    base_url="https://api.groq.com/openai/v1",
                    api_key=os.environ["GROQ_API_KEY"],
                    verbose=True,
                )
            case "openai":
                self.llm = LLM(
                    model=openai_model,
                    temperature=0.1,
                    api_key=os.environ["OPENAI_API_KEY"],
                    verbose=True,
                )
                self.reporter_llm = LLM(
                    model=openai_model,
                    temperature=0.7,
                    api_key=os.environ["OPENAI_API_KEY"],
                    verbose=True,
                )
            case "azure":
                self.llm = LLM(
                    model="azure/" + os.environ["AZURE_OPENAI_DEPLOYMENT"],
                    temperature=0.1,
                    base_url=os.environ["AZURE_API_BASE"],
                    api_key=os.environ["AZURE_API_KEY"],
                    verbose=True,
                )
                self.reporter_llm = LLM(
                    model="azure/" + os.environ["AZURE_OPENAI_DEPLOYMENT"],
                    temperature=0.7,
                    base_url=os.environ["AZURE_API_BASE"],
                    api_key=os.environ["AZURE_API_KEY"],
                    verbose=True,
                )

    """
    Creates and returns an instance of the Agent class configured as a campaign manager.

    This method retrieves the configuration for the campaign manager from the 
    agents_config dictionary, initializes an Agent with the specified configuration, 
    and enables memory for the agent.

    Returns:
        Agent: An instance of the Agent class configured as a campaign manager.
    """

    @agent
    def campaign_manager(self) -> Agent:
        config = self.agents_config["campaign_manager"]
        return Agent(
            config=config,
            llm=self.llm,
            memory=True,
        )

    @agent
    def visualizer_agent(self) -> Agent:
        """
        Creates and returns a visualizer agent.

        The visualizer agent is configured using the settings from the
        'visualizer_agent' section of the agents configuration. It is equipped
        with tools for generating pie charts and bar charts.

        Returns:
            Agent: An instance of the Agent class configured with visualization tools.
        """

        config = self.agents_config["visualizer_agent"]
        return Agent(config=config, llm=self.llm)

    @agent
    def campaign_reporter_agent(self) -> Agent:
        """
        Creates and returns an instance of the campaign reporter agent.

        This agent is configured using the settings specified in the
        `agents_config` dictionary under the key "campaign_reporter_agent".
        It is equipped with tools for reading directories and files,
        and utilizes the specified language model (llm).

        Returns:
            Agent: An instance of the campaign reporter agent.
        """
        config = self.agents_config["campaign_reporter_agent"]
        return Agent(config=config, llm=self.reporter_llm)

    @task
    def fetch_campaigns_task(self) -> Task:
        """
        Creates and returns a Task for fetching campaigns.

        This method initializes a Task object configured to fetch campaign data.
        The task is set up with specific configurations, output file location,
        tools required for the task, the agent responsible for managing the campaigns,
        and the expected output format.

        Returns:
            Task: A configured Task object for fetching campaigns.
        """
        return Task(
            config=self.tasks_config["fetch_campaigns_task"],
            output_file=f"output/campaigns.py",
            create_directory=True,
            tools=[
                AccountCampaignsTool(),
            ],
            agent=self.campaign_manager(),
            pydantic=CampaignList,
            # human_input=True,
        )

    @task
    def campaigns_budget_pie_chart(self) -> Task:
        """
        Creates a Task to generate a pie chart visualizing campaign budgets.

        This method configures a Task using the "campaigns_budget_pie_chart"
        settings from the tasks configuration. It utilizes the PieChartTool
        for creating the pie chart and the visualizer agent for rendering.
        The context is enhanced by including the result of the fetch_campaigns_task
        method to ensure consistency.

        Returns:
            Task: A configured Task object for generating the campaigns budget pie chart.
        """
        return Task(
            config=self.tasks_config["campaigns_budget_pie_chart"],
            tools=[
                PieChartTool(),
            ],
            agent=self.visualizer_agent(),
            context=[self.fetch_campaigns_task()],  # context improves consistency
        )

    @task
    def campaigns_report(self) -> Task:
        """
        Generates a Task for creating a campaigns report.
        This is a simple example of a markdown report that lists the campaigns.

        Returns:
            Task: A Task object configured to generate a campaigns report.
        """
        return Task(
            config=self.tasks_config["campaigns_report"],
            output_file=f"output/campaigns_report.md",
            create_directory=True,
            agent=self.campaign_reporter_agent(),
            # asynch=True,
            context=[  # context improves consistency
                self.fetch_campaigns_task(),
                self.campaigns_budget_pie_chart(),
            ],
            tools=[SumListTool()],
            # human_input=True
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates and returns a Crew instance with the specified configuration.
        Returns:
            Crew: An instance of the Crew class initialized with the current
                  agents, tasks, and other parameters.
        """

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=self.llm,
            output_log_file=f"output/part_2.log",
            output=f"output/part_2.md",
            create_directory=True,
        )

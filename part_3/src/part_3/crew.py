from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from part_3.tools.analytics import (
    CampaignAnalyticsTool,
    DownloadReportTool,
    ReportStatusTool,
)
from part_3.tools.auth import AuthTool
from part_3.tools.campaigns import CampaignsTool

auth = AuthTool()
auth_response = auth._run()
token = auth_response["access_token"]


@CrewBase
class Part3Crew:
    """Part 3 crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def campaign_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_manager"],
            tools=[CampaignsTool(token=token)],
            verbose=True,
            cache=True,
            memory=True,
        )

    @agent
    def campaign_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["campaign_reporter"],
            tools=[
                CampaignAnalyticsTool(token=token),
                ReportStatusTool(token=token),
                DownloadReportTool(token=token),
            ],
            verbose=True,
            max_iter=2,
            max_rpm=5,
            memory=True,
        )

    # @agent
    # def researcher(self) -> Agent:
    # 	return Agent(
    # 		config=self.agents_config['researcher'],
    # 		verbose=True
    # 	)

    # @agent
    # def reporting_analyst(self) -> Agent:
    # 	return Agent(
    # 		config=self.agents_config['reporting_analyst'],
    # 		verbose=True
    # 	)

    @task
    def campaigns(self) -> Task:
        return Task(
            config=self.tasks_config["campaigns"],
            cache=True,
            output_file="output/campaign_ids.json",
        )

    @task
    def create_impressions_report(self) -> Task:
        return Task(
            config=self.tasks_config["create_impressions_report"],
            output_file="output/create_report_.json",
        )

    iter

    @task
    def check_report_status(self) -> Task:
        return Task(
            config=self.tasks_config["check_report_status"],
            output_file="output/report_status.json",
        )

    @task
    def download_report(self) -> Task:
        return Task(
            config=self.tasks_config["download_report"],
            cache=True,
            output_file="output/campaign_report.json",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Part 3 crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=ChatOpenAI(model="gpt-4o-mini"),
            output_log_file="output/part_3.log",
            output_file="output/part_3.md",
        )

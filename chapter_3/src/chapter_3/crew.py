from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from chapter_3.tools.analytics import CampaignAnalyticsTool, DownloadReportTool, ReportStatusTool
from chapter_3.tools.auth import AuthTool
from chapter_3.tools.campaigns import CampaignsTool

auth = AuthTool()
auth_response = auth._run()
token = auth_response['access_token']

@CrewBase
class Chapter3Crew():
	"""Chapter 3 crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	
	@agent
	def campaign_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['campaign_manager'],
			tools=[CampaignsTool(token=token)],
			verbose=True,
			cache=True
		)
	
	@agent
	def campaign_reporter(self) -> Agent:
		return Agent(
			config=self.agents_config['campaign_reporter'],
			tools=[CampaignAnalyticsTool(token=token), ReportStatusTool(token=token), DownloadReportTool(token=token)],
			verbose=True,
			
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
			config=self.tasks_config['campaigns'],
			cache=True,
		)

	@task
	def check_report_status(self) -> Task:
		return Task(
			config=self.tasks_config['check_report_status'],
		)
	
	@task
	def create_impressions_report(self) -> Task:
		return Task(
			config=self.tasks_config['create_impressions_report'],
		)
	
	@task
	def download_report(self) -> Task:
		return Task(
			config=self.tasks_config['download_report'],
			cache=True,
			outout_file='output/campaign_report.json'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Chapter 3 crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			planning=True,
			outout_file='output/chapter_3.md'
		)
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from chapter_1.tools.auth import AuthTool
from chapter_1.tools.accounts import AccountsTool, RetailersTool, BrandsTool

auth = AuthTool()
auth_response = auth._run()
token = auth_response['access_token']

@CrewBase
class Chapter1Crew():
	"""Chapter 1 crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def account_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['account_manager'],
			tools=[AccountsTool(token=token), RetailersTool(token=token), BrandsTool(token=token)],
			verbose=True,
			cache=True
		)

	@task
	def accounts(self) -> Task:
		return Task(
			config=self.tasks_config['accounts'],
			output_file='output/accounts.md'
		)

	@task
	def brands(self) -> Task:
		return Task(
			config=self.tasks_config['brands'],
			output_file='output/brands.md',
		)

	@task
	def retailers(self) -> Task:
		return Task(
			config=self.tasks_config['retailers'],
			output_file='output/retailers.md',
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Chapter 1 crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
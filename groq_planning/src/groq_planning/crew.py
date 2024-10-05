import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from litellm import GroqChatCompletion, completion
from langchain_groq import ChatGroq

# Uncomment the following line to use an example of a custom tool
# from groq_planning.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class GroqPlanningCrew():
	"""GroqPlanning crew"""

	def __init__(self):

		print("+++++++++++ Groq +++++++++++")
		print("GROQ_AI_MODEL_NAME",os.environ["GROQ_AI_MODEL_NAME"])
		print("GROQ_API_KEY",os.environ["GROQ_API_KEY"])

		self.lite = LLM(
			model="groq/llama-3.1-70b-versatile",
			temperature=0.7,
			base_url="https://api.groq.com/openai/v1",
			api_key=os.environ["GROQ_API_KEY"],
		)
		if self.lite:
			print("Groq LLM created - testing...")
			response = completion(
				model="groq/llama-3.1-70b-versatile", 
				messages=[
				{"role": "user", "content": "tell me a dad joke"}
			],
			)
			print("groq test respoinse:",response)
			print("\n\n")

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=self.lite
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=self.lite
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the GroqPlanning crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			# planning=True,
			# planning_llm=self.llm
		)

		# pleanning does not work with Groq
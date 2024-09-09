import os
from crewai import Agent, Process, Task, Crew
from crewai.project import CrewBase, agent, crew, task


from langchain.chat_models.azure_openai import AzureChatOpenAI

# Configure the Azure OpenAI model
llm = AzureChatOpenAI(
    model="gpt-4o", deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"]
)


@CrewBase
class AzureExample:

    # Create an agent
    @agent
    def expert(self) -> Agent:
        return Agent(
            role="Local Expert",
            goal="Provide insights about the city",
            backstory="A knowledgeable local guide.",
            verbose=True,
            llm=llm,
        )

    # Create a task for the agent
    @task
    def research(self) -> Task:
        return Task(
            description="What are the best places to visit in Paris?",
            agent=self.expert(),
            expected_output="A list of top tourist attractions.",
            output_file="output/tourist_attractions.txt",
        )

    # Create a crew and add the agent and task
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,
            output_log_file="output/azure_example.log",
        )


# Execute the task
# result = crew.kickoff()
# print(result)

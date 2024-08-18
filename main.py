import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI


from textwrap import dedent
from agents import RetailMediaAgents
from tasks import RetailMediaTasks

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

from langchain.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()


# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py


class RetailMediaCrew:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = RetailMediaAgents()
        tasks = RetailMediaTasks()

        # Define your custom crew here
        crew = Crew(
            agents=[agents],
            tasks=[tasks],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that will run the crew.
if __name__ == "__main__":
    print("## Welcome to Retail Media Crew AI")
    print("-------------------------------")
    var1 = input(dedent("""Enter variable 1: """))
    var2 = input(dedent("""Enter variable 2: """))

    crew = RetailMediaCrew(var1, var2)
    result = crew.run()
    print("\n\n########################")
    print("## Here is you Retail Media crew run result:")
    print("########################\n")
    print(result)
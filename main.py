import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from textwrap import dedent
from crew import RetailMediaCrew

from dotenv import load_dotenv

load_dotenv()


# This is the main function that will run the crew.
if __name__ == "__main__":
    print("## Welcome to Retail Media Crew AI")
   

    result = RetailMediaCrew().crew().kickoff()
    print("\n\n############################################")
    print("## Here is you Retail Media crew run result:")
    print("############################################\n")
    print(result)
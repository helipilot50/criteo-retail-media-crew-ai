import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from textwrap import dedent
from crew_one import crew as crew_1

from dotenv import load_dotenv

load_dotenv()


# This is the main function that will run the crew.
if __name__ == "__main__":
    print("## Welcome to Retail Media Crew AI")
   

    result = crew_1.kickoff()
    print("\n\n############################################")
    print("## Retail Media crew rcompleted")
    print("############################################\n")
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from textwrap import dedent
from crew_one import crew as crew_1
from crew_two import crew as crew_2
from crew_three import crew as crew_3

from dotenv import load_dotenv

load_dotenv()


# This is the main function that will run the crew.
if __name__ == "__main__":
    print("## Welcome to Retail Media Crew AI")

    result = crew_3.kickoff()
    print("\n\n############################################")
    print("## Retail Media crew rcompleted")
    print("############################################\n")
    print(result)

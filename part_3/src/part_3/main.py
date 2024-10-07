#!/usr/bin/env python
import sys
from part_3.crew import Part3Crew

from dotenv import load_dotenv

load_dotenv()

artist_name = input("Enter the artist name (default: 'Ed Sheeran'): ") or "Ed Sheeran"
year = input("Enter the year (Default: 2025): ") or "2025"
account_id = input("Enter the account id (Default: 4): ") or 4
digital_advertising_budget = input("Enter the digital advertising budget (Default: 500000): ") or 500000

inputs = {"account_id": account_id, 
          "artist_name": artist_name, 
          "year": year, 
          "digital_advertising_budget": digital_advertising_budget}

print(f"Inputs: {inputs}")

def run():
    """
    Run the crew.
    """

    Part3Crew(inputs=inputs).crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Part3Crew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Part3Crew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"account id": "26"}
    try:
        Part3Crew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

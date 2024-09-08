#!/usr/bin/env python
import sys
from part_2.crew import Part2Crew

from dotenv import load_dotenv

load_dotenv()


def run():

    """
    User inputs the account ID
    """
    account_id = input("Account ID: ")
    print("Running crew for account id: " + account_id )

    inputs = {"account_id": str(account_id)}

    """
    Run the crew.
    """
    Part2Crew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Part2Crew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2])

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Part2Crew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        Part2Crew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2]
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

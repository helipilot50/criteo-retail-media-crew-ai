#!/usr/bin/env python
import sys
from part_3.crew import Part3Crew

from dotenv import load_dotenv

load_dotenv()

inputs = {"account_id": "4", "artist_name": "Taylor Swift", "year": "2025"}


def run():
    """
    Run the crew.
    """
    inputs = {"account_id": "4", "artist_name": "Taylor Swift", "year": "2025"}
    Part3Crew().crew().kickoff(inputs=inputs)


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

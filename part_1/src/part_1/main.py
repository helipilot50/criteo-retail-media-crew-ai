#!/usr/bin/env python
import sys
from part_1.crew import Part1Crew

# This main file is run your crew locally,
# it will automatically interpolate any tasks and agents information

from dotenv import load_dotenv

load_dotenv()


def run():
    """
    Run the crew.
    """
    Part1Crew().crew().kickoff()


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Part1Crew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2])

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Part1Crew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        Part1Crew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2]
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

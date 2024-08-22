#!/usr/bin/env python
import sys
from chapter_2.crew import Chapter2Crew

from dotenv import load_dotenv

load_dotenv()

def run():
    """
    Run the crew.
    """
    Chapter2Crew().crew().kickoff()


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Chapter2Crew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2])

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Chapter2Crew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        Chapter2Crew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

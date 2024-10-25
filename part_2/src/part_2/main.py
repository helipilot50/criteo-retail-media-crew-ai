#!/usr/bin/env python
import sys
from part_2.crew import Part2Crew
from part_2.llm_chooser import choose_llm
from part_2.tools.accounts import choose_account
import os
from dotenv import load_dotenv

load_dotenv()

"""
LLM service chooser
"""

target_llm = choose_llm()

"""
The account ID
"""

account = choose_account()

inputs = {"account_id": account.id, "target_llm": target_llm.lower()}


def run():
    """
    Run the crew.
    """

    Part2Crew(inputs=inputs).crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Part2Crew(inputs=inputs).crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Part2Crew(inputs=inputs).crew().replay(task_id=sys.argv[1], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        Part2Crew(inputs=inputs).crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

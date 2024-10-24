#!/usr/bin/env python
import sys
from part_3.crew import Part3Crew
from part_3.llm_chooser import choose_llm
from part_3.tools.accounts import choose_account
from dotenv import load_dotenv

load_dotenv()

artist_name = input("Enter the artist name (default: 'Ed Sheeran'): ") or "Ed Sheeran"
year = input("Enter the year (Default: 2025): ") or "2025"
account = choose_account()
digital_advertising_budget = (
    input("Enter the digital advertising budget (Default: 500000): ") or 500000
)


target_llm = choose_llm()


inputs = {
    "account_id": account.id,
    "artist_name": artist_name,
    "year": year,
    "digital_advertising_budget": digital_advertising_budget,
    "target_llm": target_llm.lower(),
}

# print(f"Inputs: {inputs}")


def run():
    """
    Run the crew.
    """

    Part3Crew(inputs=inputs, account=account).crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        Part3Crew(inputs=inputs, account=account).crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Part3Crew(inputs=inputs, account=account).crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"account id": "26"}
    try:
        Part3Crew(inputs=inputs, account=account).crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

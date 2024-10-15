#!/usr/bin/env python
import sys
from part_1.crew import Part1Crew

# This main file is run your crew locally,
# it will automatically interpolate any tasks and agents information

from dotenv import load_dotenv

load_dotenv()

"""
LLM service chooser
"""


def display_menu(options):
    print("Please select an LLM:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")


def get_user_choice(options, default=None):
    while True:
        try:
            choice = input(f"Enter the number of LLM (default is {default}): ")
            if choice == "" and default is not None:
                return options[default - 1]
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


options = ["groq", "azure"]
display_menu(options)
groq_or_azure = get_user_choice(options, default=1)

inputs = {"groq_or_azure": groq_or_azure.lower()}


def run():
    """
    Run the crew.
    """
    Part1Crew(inputs=inputs).crew().kickoff()


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

#!/usr/bin/env python
import sys
from part_3.crew import Part3Crew

from dotenv import load_dotenv

load_dotenv()

"""
LLM service chooser
"""
def display_menu(options):
    print("Please select an option:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
def get_user_choice(options, default=None):
    while True:
        try:
            choice = input(f"Enter the number of your choice (default is {default}): ")
            if choice == "" and default is not None:
                return options[default - 1]
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# user inputthe linitem_id
artist_name = input("Enter the artist name (default: 'Ed Sheeran'): ") or "Ed Sheeran"
year = input("Enter the year (Default: 2025): ") or "2025"
account_id = input("Enter the account id (Default: 4): ") or 4
digital_advertising_budget = input("Enter the digital advertising budget (Default: 500000): ") or 500000

options = ["azure", "groq"]
display_menu(options)
groq_or_azure = get_user_choice(options, default=1)
# goodgroq_or_azure = input("Groq or Azure (Default: 'Azure'): ") or "azure"

inputs = {"account_id": account_id, 
          "artist_name": artist_name, 
          "year": year, 
          "digital_advertising_budget": digital_advertising_budget,
          "groq_or_azure": groq_or_azure.lower()}

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
        Part3Crew(inputs=inputs).crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Part3Crew(inputs=inputs).crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"account id": "26"}
    try:
        Part3Crew(inputs=inputs).crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

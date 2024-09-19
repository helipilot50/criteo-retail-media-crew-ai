import json

from dotenv import load_dotenv

load_dotenv()

import panel as pn
from crewai.agents import CrewAgentExecutor
import threading
import time
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
from part_3.crew import Part3Crew


pn.extension(design="material")

user_input = None
initiate_chat_task_created = False
chat_interface = None


def custom_ask_human(self, final_answer: dict) -> str:

    global user_input

    prompt = self._i18n.slice("getting_input").format(final_answer=final_answer)

    chat_interface.send(prompt, user="assistant", respond=False)

    while user_input == None:
        time.sleep(1)

    human_comments = user_input
    user_input = None

    return human_comments


# def StartCrew(prompt:str):
def StartCrew(account_id: str):
    CrewAgentExecutor._ask_human_input = custom_ask_human

    global chat_interface

    inputs = {"account_id": account_id}

    result = Part3Crew(instance=chat_interface).crew().kickoff(inputs=inputs)
    chat_interface.send(
        "## Final Result\n" + str(result), user="assistant", respond=False
    )


def initiate_chat(account_id: str):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True

    print("--- initiate_chat ---")
    print("account_id: ", account_id)

    StartCrew(account_id)


def callback(input: str, user: str, whatt:any):

    global initiate_chat_task_created
    global user_input

    print("--- callback ---")
    print("input: ", input)
    print("user: ", user)
    # print("whatt: ", whatt)

    if not initiate_chat_task_created:
        thread = threading.Thread(target=initiate_chat, args=(input))
        thread.start()

    else:
        user_input = input


def main():
    print("*************** Start Panel Application ***************")

    global chat_interface
    chat_interface = pn.chat.ChatInterface(callback=callback)
    image_path = "images/ticket_marketing_logo.jpeg"
    image_widget = pn.pane.JPG(image_path, width=100, height=100)
    chat_interface.append(image_widget)
    text_widget = pn.pane.Markdown(
        """
        # Welcome to the Ticket Campaign assistant. 
        when asked, please enter the account ID 
        """
    )
    chat_interface.append(text_widget)
    chat_interface.send(
        "Are you ready to begin? Enter the account ID", user="System", respond=False
    )

    chat_interface.servable()


main()

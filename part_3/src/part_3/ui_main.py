import json

from dotenv import load_dotenv

load_dotenv()

import panel as pn
import datetime as dt
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
def StartCrew(account_id: str, artist_name: str, year: str):
    CrewAgentExecutor._ask_human_input = custom_ask_human

    global chat_interface

    inputs = {"account_id": account_id, "artist_name": artist_name, "year": year}

    result = Part3Crew(instance=chat_interface).crew().kickoff(inputs=inputs)
    chat_interface.send(
        "## Final Result\n" + str(result), user="assistant", respond=False
    )


def initiate_chat(account_id: str, artist_name: str, year: str):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True

    print("--- initiate_chat ---")
    print("account_id: ", account_id)
    print("artist_name: ", artist_name)
    print("year: ", year)

    StartCrew(account_id, artist_name, year)


def callback(input: str, user: str, whatt: any):

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
    account_input = pn.widgets.TextInput(
        name="Account ID:", placeholder="account ID here..."
    )
    artist_name_input = pn.widgets.TextInput(
        name="Artist Name:", placeholder="artist name here..."
    )

    go_button = pn.widgets.Button(name="Go", button_type="primary")
    year_input = pn.widgets.TextInput(name="Year:", placeholder="year here...")
    chat_interface.append(text_widget)
    chat_interface.append(account_input)
    chat_interface.append(artist_name_input)
    chat_interface.append(year_input)
    chat_interface.append(go_button)

    def on_go_click(event):
        account_id = account_input.value
        artist_name = artist_name_input.value
        year = year_input.value
        print("--- on_go_click ---", event)
        print("account_id: ", account_id)
        print("artist_name: ", artist_name)
        print("year: ", year)
        # initiate_chat(account_id, artist_name, year)

    go_button.on_click(on_go_click)
    # chat_interface.send("Enter the account ID", user="System", respond=True)

    # chat_interface.servable()
    chat_interface.show()


main()

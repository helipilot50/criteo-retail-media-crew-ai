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

def custom_ask_human(self, final_answer:dict)->str:
    global user_input

    global user_input

    prompt = self._i18n.slice("getting_input").format(final_answer=final_answer)

    chat_interface.send(prompt, user="assistant", respond=False)

    while user_input == None:
        time.sleep(1)  

    human_comments = user_input
    user_input = None

    return human_comments


user_input = None
initiate_chat_task_created = False

def initiate_chat(message):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True

    StartCrew(message)

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    
    global initiate_chat_task_created
    global user_input

    if not initiate_chat_task_created:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()

    else:
        user_input = contents

global chat_interface
chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Enter the account ID", user="System", respond=False)
chat_interface.servable()

def StartCrew(prompt:str):

    CrewAgentExecutor._ask_human_input = custom_ask_human

    inputs = {"accountId": prompt}

    result = Part3Crew(instance = chat_interface).crew().kickoff(inputs=inputs)

    chat_interface.send("## Final Result\n"+str(result), user="assistant", respond=False)



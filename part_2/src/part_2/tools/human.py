import chainlit as cl
from chainlit import run_sync
from crewai import Agent, Task, Crew
from crewai_tools import tool

@tool("Ask Human follow up questions")
def ask_human(question: str) -> str:
    """Ask human follow up questions"""
    human_response  = run_sync( cl.AskUserMessage(content=f"{question}").send())
    if human_response:
        return human_response["output"]
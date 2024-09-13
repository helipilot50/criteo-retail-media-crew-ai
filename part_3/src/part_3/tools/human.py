import streamlit as st
from chainlit import run_sync
from crewai import Agent, Task, Crew
from crewai_tools import BaseTool

"""
Ask Human for decision and help using streamlit.

Attributes:
    name (str): The name of the tool.
    description (str): The description of the tool.

Methods:
    _run(question: str) -> str: Runs the tool and asks the human a question for decision and help using streamlit.

Returns:
    str: The answer provided by the human.
"""
class StreamlitHumanTool(BaseTool):
    name: str = "Ask Human for decision and help"
    description: str = "Ask Human a question for decision and help using streamlit"
    def _run(self, question: str):
        st.chat_message("user").write(f"{question}")
        answer = st.chat_input()
        return answer


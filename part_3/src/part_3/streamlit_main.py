#!/usr/bin/env python
"""
This script runs a Streamlit application for Part 3 - Automated Campaign and Lineitems.
Usage:
    streamlit run streamlit_main.py
Author:
    Peter Milne
"""
import sys
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from part_3.crew import Part3Crew



def run():
    """
    This function runs a Streamlit application for Part 3 - Automated Campaign and Lineitems.
    Usage:
        streamlit run streamlit_main.py
    Author:
        Peter Milne
    """
    # Streamlit UI setup
    st.title("Part 3 - Automated Campaign and Lineitems") 

    # Initialize the message log in session state if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "crew", "content": "Enter the Account ID?"}]

    # Display existing messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle user input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": f"Working on account: {prompt}"})
        st.chat_message("user").write(f"Working on account: {prompt}")
   
    # Run the crew.
    inputs = {"account_id": prompt }
    
    final_result = Part3Crew().crew().kickoff(inputs=inputs)

    st.session_state.messages.append({"role": "assistant", "content": final_result})
    st.chat_message("assistant").write(final_result)



if __name__ == '__main__':
    run()

# streamlit run main.py
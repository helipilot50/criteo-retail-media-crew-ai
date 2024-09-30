import os
import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model=os.environ["GROQ_AI_MODEL_NAME"],
    api_key=os.environ["GROQ_API_KEY"],
)

print("llm",llm)
import os
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def azure():
    print("+++++++++++ Azure OpenAI +++++++++++")
    print("AZURE_OPENAI_API_VERSION", os.environ["AZURE_OPENAI_API_VERSION"])
    print(
        "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME",
        os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )
    print("AZURE_OPENAI_ENDPOINT", os.environ["AZURE_OPENAI_ENDPOINT"])
    print("AZURE_OPENAI_API_KEY", os.environ["AZURE_OPENAI_API_KEY"])
    azure_llm = AzureChatOpenAI(
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        max_tokens=4096,
        max_retries=2,
        temperature=0.6,
    )
    pi = azure_llm.invoke("what is PI to 10 decimal places")
    print("PI", pi)


def groq():
    print("+++++++++++ Groq +++++++++++")
    print("GROQ_AI_MODEL_NAME", os.environ["GROQ_AI_MODEL_NAME"])
    print("GROQ_API_KEY", os.environ["GROQ_API_KEY"])
    llm = ChatGroq(
        model=os.environ["GROQ_AI_MODEL_NAME"],
        api_key=os.environ["GROQ_API_KEY"],
    )

    print("llm", llm)

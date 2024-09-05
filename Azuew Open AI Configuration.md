# Azure Open AI Configuration¶

For Azure OpenAI API integration, set the following environment variables:

```
os.environ[AZURE_OPENAI_DEPLOYMENT] = "Your deployment"
os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "Your Endpoint"
os.environ["AZURE_OPENAI_API_KEY"] = "<Your API Key>"
```

## Example Agent with Azure LLM

```
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import AzureChatOpenAI

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

azure_agent = Agent(
  role='Example Agent',
  goal='Demonstrate custom LLM configuration',
  backstory='A diligent explorer of GitHub docs.',
  llm=azure_llm
)
```

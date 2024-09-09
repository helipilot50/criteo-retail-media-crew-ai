# Azure Open AI Configuration¶

## Example Agent with Azure LLM

```
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import AzureChatOpenAI


from langchain_openai import AzureChatOpenAI

azure_llm = AzureChatOpenAI(
    model="gpt-4o", deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"]
)

azure_agent = Agent(
  role='Example Agent',
  goal='Demonstrate custom LLM configuration',
  backstory='A diligent explorer of GitHub docs.',
  llm=azure_llm
)
```

## References

- [Azure OpenAI service documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)
- [FAQ](https://learn.microsoft.com/en-us/azure/ai-services/openai/faq)

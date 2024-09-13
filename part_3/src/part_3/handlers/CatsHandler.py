from langchain.callbacks.base import BaseCallbackHandler

class MyCallbackHandler(BaseCallbackHandler):
    def on_agent_action(self, action, **kwargs):
        print(f"Agent action: {action}")

    def on_agent_finish(self, finish, **kwargs):
        print(f"Agent finished: {finish}")

    def on_llm_new_token(self, token, **kwargs):
        print(f"New token: {token}")

    def on_llm_end(self, response, **kwargs):
        print(f"LLM response: {response}")



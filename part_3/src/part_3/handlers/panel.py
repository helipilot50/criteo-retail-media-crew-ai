from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.agents import AgentFinish
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import UUID
import panel as pn

avators = {"Writer":"https://cdn-icons-png.flaticon.com/512/320/320336.png",
            "Reviewer":"https://cdn-icons-png.freepik.com/512/9408/9408201.png"}

class PanelHandler(BaseCallbackHandler):
    
    def __init__(self, agent_name: str, instance: pn.chat.ChatInterface) -> None:
        self.agent_name = agent_name
        self.instance = instance
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""

        self.instance.send(inputs['input'], user="assistant", respond=False)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        
        self.instance.send(outputs['output'], user=self.agent_name, avatar=avators[self.agent_name], respond=False)

    def on_agent_action(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """""Log the action taken by an agent during a chain run."""
        print(f"{self.agent_name} is working on the task....")

    def on_agent_finish(self, finish: AgentFinish, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
        """Log the finish of an agent."""
        print(f"{self.agent_name} has finished working on the task....")
    
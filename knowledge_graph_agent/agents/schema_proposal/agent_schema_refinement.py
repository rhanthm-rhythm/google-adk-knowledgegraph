from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.base_agent import BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents import LoopAgent
from typing import AsyncGenerator

from knowledge_graph_agent.callbacks.log_agent_callback import log_agent
from knowledge_graph_agent.agents.schema_proposal.agent_schema_proposal import schema_proposal_agent
from knowledge_graph_agent.agents.schema_proposal.agent_schema_critic import schema_critic_agent

class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        feedback = ctx.session.state.get("feedback", "valid")
        should_stop = (feedback == "valid")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

schema_refinement_loop = LoopAgent(
    name="schema_refinement_loop",
    description="Analyzes approved files to propose a schema based on user intent and feedback",
    max_iterations=2,
    sub_agents=[schema_proposal_agent, schema_critic_agent, CheckStatusAndEscalate(name="StopChecker")],
    before_agent_callback=log_agent
)

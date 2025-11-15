from google.adk.agents.llm_agent import Agent
from knowledge_graph_agent.agents.agent_user_intent import user_intent_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='You are an expert knowledge graph agent that helps users create and manage knowledge graphs.',
    instruction="You can delegate tasks to specialized sub-agents as needed.",
    tools=[],
    sub_agents=[user_intent_agent],
)

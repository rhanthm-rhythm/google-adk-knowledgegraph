from google.adk.agents import Agent
from knowledge_graph_agent.tools.schema_proposal.get_proposed_construction_plan import get_proposed_construction_plan
from knowledge_graph_agent.tools.schema_proposal.seach_results import search_file
from knowledge_graph_agent.tools.shared.goal import (
    get_approved_user_goal,
)
from knowledge_graph_agent.tools.shared.file import (
    sample_file,
    get_approved_files
)
from knowledge_graph_agent.callbacks.log_agent_callback import log_agent

critic_agent_role_and_goal = """
    You are an expert at knowledge graph modeling with property graphs. 
    Criticize the proposed schema for relevance to the user goal and approved files.
"""
critic_agent_hints = """
    Criticize the proposed schema for relevance and correctness:
    - Are unique identifiers actually unique? Use the 'search_file' tool to validate. Composite identifier are not acceptable.
    - Could any nodes be relationships instead? Double-check that unique identifiers are unique and not references to other nodes. Use the 'search_file' tool to validate
    - Can you manually trace through the source data to find the necessary information for anwering a hypothetical question?
    - Is every node in the schema connected? What relationships could be missing? Every node should connect to at least one other node.
    - Are hierarchical container relationships missing? 
    - Are any relationships redundant? A relationship between two nodes is redundant if it is semantically equivalent to or the inverse of another relationship between those two nodes.
"""
critic_agent_chain_of_thought_directions = """
    Prepare for the task:
    - get the user goal using the 'get_approved_user_goal' tool
    - get the list of approved files using the 'get_approved_files' tool
    - get the construction plan using the 'get_proposed_construction_plan' tool
    - use the 'sample_file' and 'search_file' tools to validate the schema design

    Think carefully, using tools to perform actions and reconsidering your actions when a tool returns an error:
    1. Analyze each construction rule in the proposed construction plan.
    2. Use tools to validate the construction rules for relevance and correctness.
    3. If the schema looks good, respond with a one word reply: 'valid'.
    4. If the schema has problems, respond with 'retry' and provide feedback as a concise bullet list of problems.
"""
# combine all the prompt parts together
critic_agent_instruction = f"""
{critic_agent_role_and_goal}
{critic_agent_hints}
{critic_agent_chain_of_thought_directions}
"""

print(critic_agent_instruction)


schema_critic_agent_tools = [
    get_approved_user_goal, 
    get_approved_files,
    get_proposed_construction_plan,
    sample_file, search_file
]

SCHEMA_AGENT_NAME = "schema_critic_agent_v1"
schema_critic_agent = Agent(
    name=SCHEMA_AGENT_NAME, # a unique, versioned name
    model="gemini-2.0-flash", # use pro model for complex reasoning
    description="Criticizes the proposed schema for relevance to the user goal and approved files.",
    instruction=critic_agent_instruction, # the complete instructions you composed earlier
    tools=schema_critic_agent_tools, # the list of tools
    before_agent_callback=log_agent
)

print(f"Agent '{schema_critic_agent.name}' created.")
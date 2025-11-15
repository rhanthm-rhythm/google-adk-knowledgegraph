from google.adk.agents import Agent
from knowledge_graph_agent.tools.shared.goal import (
    set_perceived_user_goal,
    approve_perceived_user_goal,
)

# define the role and goal for the user intent agent
agent_role_and_goal = """
    You are an expert at knowledge graph use cases. 
    Your primary goal is to help the user come up with a knowledge graph use case.
"""
# give the agent some hints about what to say
agent_conversational_hints = """
    If the user is unsure what to do, make some suggestions based on classic use cases like:
    - social network involving friends, family, or professional relationships
    - logistics network with suppliers, customers, and partners
    - recommendation system with customers, products, and purchase patterns
    - fraud detection over multiple accounts with suspicious patterns of transactions
    - pop-culture graphs with movies, books, or music
"""
# describe what the output should look like
agent_output_definition = """
    A user goal has two components:
    - kind_of_graph: at most 3 words describing the graph, for example "social network" or "USA freight logistics"
    - description: a few sentences about the intention of the graph, for example "A dynamic routing and delivery system for cargo." or "Analysis of product dependencies and supplier alternatives."
"""
# specify the steps the agent should follow
agent_chain_of_thought_directions = """
    Think carefully and collaborate with the user:
    1. Understand the user's goal, which is a kind_of_graph with description
    2. Ask clarifying questions as needed
    3. When you think you understand their goal, use the 'set_perceived_user_goal' tool to record your perception
    4. Present the perceived user goal to the user for confirmation
    5. If the user agrees, use the 'approve_perceived_user_goal' tool to approve the user goal. This will save the goal in state under the 'approved_user_goal' key.
"""
# combine all the instruction components into one complete instruction...
complete_agent_instruction = f"""
{agent_role_and_goal}
{agent_conversational_hints}
{agent_output_definition}
{agent_chain_of_thought_directions}
"""

user_intent_agent_tools = [set_perceived_user_goal, approve_perceived_user_goal]
user_intent_agent = Agent(
    name="user_intent_agent_v1", # a unique, versioned name
    model="gemini-2.5-flash", # defined earlier in a variable
    description="Helps the user ideate on a knowledge graph use case.", # used for delegation
    instruction=complete_agent_instruction, # the complete instructions you composed earlier
    tools=user_intent_agent_tools, # the list of tools
)

print(f"Agent '{user_intent_agent.name}' created.")
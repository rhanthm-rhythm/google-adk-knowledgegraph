from google.adk.agents import Agent
from knowledge_graph_agent.tools.schema_proposal.get_proposed_construction_plan import get_proposed_construction_plan
from knowledge_graph_agent.tools.schema_proposal.propose_node_construction import propose_node_construction
from knowledge_graph_agent.tools.schema_proposal.propose_relationship_construction import propose_relationship_construction
from knowledge_graph_agent.tools.schema_proposal.remove_node_construction import remove_node_construction
from knowledge_graph_agent.tools.schema_proposal.remove_relationship_construction import remove_relationship_construction
from knowledge_graph_agent.tools.schema_proposal.seach_results import search_file
from knowledge_graph_agent.tools.shared.goal import (
    get_approved_user_goal,
)
from knowledge_graph_agent.tools.shared.file import (
    sample_file,
    get_approved_files
)
from knowledge_graph_agent.callbacks.log_agent_callback import log_agent

# define the role and goal for the user intent agent
agent_role_and_goal = """
    You are an expert at knowledge graph modeling with property graphs. Propose an appropriate
    schema by specifying construction rules which transform approved files into nodes or relationships.
    The resulting schema should describe a knowledge graph based on the user goal.
    
    Consider feedback if it is available: 
    <feedback>
    {feedback}
    </feedback> 
"""
# give the agent some hints about what to say
agent_hints = """
    Every file in the approved files list will become either a node or a relationship.
    Determining whether a file likely represents a node or a relationship is based
    on a hint from the filename (is it a single thing or two things) and the
    identifiers found within the file.

    Because unique identifiers are so important for determining the structure of the graph,
    always verify the uniqueness of suspected unique identifiers using the 'search_file' tool.

    General guidance for identifying a node or a relationship:
    - If the file name is singular and has only 1 unique identifier it is likely a node
    - If the file name is a combination of two things, it is likely a full relationship
    - If the file name sounds like a node, but there are multiple unique identifiers, that is likely a node with reference relationships

    Design rules for nodes:
    - Nodes will have unique identifiers. 
    - Nodes _may_ have identifiers that are used as reference relationships.

    Design rules for relationships:
    - Relationships appear in two ways: full relationships and reference relationships.

    Full relationships:
    - Full relationships appear in dedicated relationship files, often having a filename that references two entities
    - Full relationships typically have references to a source and destination node.
    - Full relationships _do not have_ unique identifiers, but instead have references to the primary keys of the source and destination nodes.
    - The absence of a single, unique identifier is a strong indicator that a file is a full relationship.
    
    Reference relationships:
    - Reference relationships appear as foreign key references in node files
    - Reference relationship foreign key column names often hint at the destination node and relationship type
    - References may be hierarchical container relationships, with terminology revealing parent-child, "has", "contains", membership, or similar relationship
    - References may be peer relationships, that is often a self-reference to a similar class of nodes. For example, "knows" or "see also"

    The resulting schema should be a connected graph, with no isolated components.
"""

proposal_agent_chain_of_thought_directions = """
    Prepare for the task:
    - get the user goal using the 'get_approved_user_goal' tool
    - get the list of approved files using the 'get_approved_files' tool
    - get the current construction plan using the 'get_proposed_construction_plan' tool

    Think carefully, using tools to perform actions and reconsidering your actions when a tool returns an error:
    1. For each approved file, consider whether it represents a node or relationship. Check the content for potential unique identifiers using the 'sample_file' tool.
    2. For each identifier, verify that it is unique by using the 'search_file' tool.
    3. Use the node vs relationship guidance for deciding whether the file represents a node or a relationship.
    4. For a node file, propose a node construction using the 'propose_node_construction' tool. 
    5. If the node contains a reference relationship, use the 'propose_relationship_construction' tool to propose a relationship construction. 
    6. For a relationship file, propose a relationship construction using the 'propose_relationship_construction' tool
    7. If you need to remove a construction, use the 'remove_node_construction' or 'remove_relationship_construction' tool
    8. When you are done with construction proposals, use the 'get_proposed_construction_plan' tool to present the plan to the user
"""
# combine all the instruction components into one complete instruction...
proposal_agent_instruction = f"""
{agent_role_and_goal}
{agent_hints}
{proposal_agent_chain_of_thought_directions}
"""

print(proposal_agent_instruction)

# List of tools for the structured schema proposal agent
structured_schema_proposal_agent_tools = [
    get_approved_user_goal, 
    get_approved_files, 
    get_proposed_construction_plan,
    sample_file, 
    search_file,
    propose_node_construction, 
    propose_relationship_construction, 
    remove_node_construction, 
    remove_relationship_construction
]

SCHEMA_AGENT_NAME = "schema_proposal_agent_v1"
schema_proposal_agent = Agent(
    name=SCHEMA_AGENT_NAME, # a unique, versioned name
    model="gemini-2.5-pro", # use pro model for complex reasoning
    description="Proposes a knowledge graph schema based on the user goal and approved file list",
    instruction=proposal_agent_instruction, # the complete instructions you composed earlier
    tools=structured_schema_proposal_agent_tools, # the list of tools
    before_agent_callback=log_agent
)

print(f"Agent '{schema_proposal_agent.name}' created.")
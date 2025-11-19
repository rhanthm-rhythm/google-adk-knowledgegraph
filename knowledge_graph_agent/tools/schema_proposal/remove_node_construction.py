from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import tool_success
from knowledge_graph_agent.tools.schema_proposal.propose_node_construction import PROPOSED_CONSTRUCTION_PLAN

# Tool: Remove Node Construction
def remove_node_construction(node_label: str, tool_context:ToolContext) -> dict:
    """Remove a node construction from the proposed construction plan based on label.

    Args:
        node_label: The label of the node construction to remove
        tool_context: The tool context

    Returns:
        dict: A dictionary containing metadata about the content.
                Includes a 'status' key ('success' or 'error').
                If 'success', includes a 'node_construction_removed' key with the label of the removed node construction
                If 'error', includes an 'error_message' key.
                The 'error_message' may have instructions about how to handle the error.
    """
    construction_plan = tool_context.state.get(PROPOSED_CONSTRUCTION_PLAN, {})
    if node_label not in construction_plan:
        return tool_success("node construction rule not found. removal not needed.")

    del construction_plan[node_label]

    tool_context.state[PROPOSED_CONSTRUCTION_PLAN] = construction_plan
    return tool_success("node_construction_removed", node_label)
from google.adk.tools import ToolContext
from knowledge_graph_agent.tools.schema_proposal.propose_node_construction import PROPOSED_CONSTRUCTION_PLAN

# Tool: Get Proposed construction Plan

def get_proposed_construction_plan(tool_context:ToolContext) -> dict:
    """Get the proposed construction plan, a dictionary of construction rules."""
    return tool_context.state.get(PROPOSED_CONSTRUCTION_PLAN, {})
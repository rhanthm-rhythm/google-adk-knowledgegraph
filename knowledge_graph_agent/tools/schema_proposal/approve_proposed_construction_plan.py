from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import tool_success, tool_error
from knowledge_graph_agent.tools.schema_proposal.propose_node_construction import PROPOSED_CONSTRUCTION_PLAN

# Tool: Approve the proposed construction plan

APPROVED_CONSTRUCTION_PLAN = "approved_construction_plan"

def approve_proposed_construction_plan(tool_context:ToolContext) -> dict:
    """Approve the proposed construction plan, if there is one."""
    if not PROPOSED_CONSTRUCTION_PLAN in tool_context.state:
        return tool_error("No proposed construction plan found. Propose a plan first.")
    
    tool_context.state[APPROVED_CONSTRUCTION_PLAN] = tool_context.state.get(PROPOSED_CONSTRUCTION_PLAN)
    return tool_success(APPROVED_CONSTRUCTION_PLAN, tool_context.state[APPROVED_CONSTRUCTION_PLAN])
    
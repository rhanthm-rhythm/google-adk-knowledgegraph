from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import tool_success, tool_error
from knowledge_graph_agent.tools.schema_proposal.get_proposed_schema import PROPOSED_SCHEMA
# Tool: Approve the proposed construction plan

APPROVED_SCHEMA= "approved_schema"

def approve_proposed_schema(tool_context:ToolContext) -> dict:
    """Approve the proposed schema, if there is one."""
    if not PROPOSED_SCHEMA in tool_context.state:
        return tool_error("No proposed schema found. Propose a schema first.")
    
    tool_context.state[APPROVED_SCHEMA] = tool_context.state.get(PROPOSED_SCHEMA)
    return tool_success(APPROVED_SCHEMA, tool_context.state[APPROVED_SCHEMA])
    
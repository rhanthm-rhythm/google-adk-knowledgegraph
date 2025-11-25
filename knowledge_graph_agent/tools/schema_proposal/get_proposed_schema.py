from google.adk.tools import ToolContext

# Tool: Get Proposed Schema
PROPOSED_SCHEMA = "proposed_schema"
def get_proposed_schema(tool_context:ToolContext) -> dict:
    """Get the proposed schema."""
    return tool_context.state.get(PROPOSED_SCHEMA, {})
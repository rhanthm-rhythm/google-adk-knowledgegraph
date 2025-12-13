from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import tool_success, tool_error

# tools to propose and approve entity types
PROPOSED_ENTITIES = "proposed_entity_types"
APPROVED_ENTITIES = "approved_entity_types"

def set_proposed_entities(proposed_entity_types: list[str], tool_context:ToolContext) -> dict:
    """Sets the list proposed entity types to extract from unstructured text."""
    tool_context.state[PROPOSED_ENTITIES] = proposed_entity_types
    return tool_success(PROPOSED_ENTITIES, proposed_entity_types)

def get_proposed_entities(tool_context:ToolContext) -> dict:
    """Gets the list of proposed entity types to extract from unstructured text."""
    return tool_context.state.get(PROPOSED_ENTITIES, [])

def approve_proposed_entities(tool_context:ToolContext) -> dict:
    """Upon approval from user, records the proposed entity types as an approved list of entity types 

    Only call this tool if the user has explicitly approved the suggested files.
    """
    if PROPOSED_ENTITIES not in tool_context.state:
        return tool_error("No proposed entity types to approve. Please set proposed entities first, ask for user approval, then call this tool.")
    tool_context.state[APPROVED_ENTITIES] = tool_context.state.get(PROPOSED_ENTITIES)
    return tool_success(APPROVED_ENTITIES, tool_context.state[APPROVED_ENTITIES])

def get_approved_entities(tool_context:ToolContext) -> dict:
    """Get the approved list of entity types to extract from unstructured text."""
    return tool_context.state.get(APPROVED_ENTITIES, [])

def get_well_known_types(tool_context:ToolContext) -> dict:
    """Gets the approved labels that represent well-known entity types in the graph schema."""
    construction_plan = tool_context.state.get("approved_construction_plan", {})
    # approved labels are the keys for each construction plan entry where `construction_type` is "node"
    approved_labels = sorted({entry["label"] for entry in construction_plan.values() if entry["construction_type"] == "node"})
    return tool_success("approved_labels", approved_labels)


from google.adk.tools import ToolContext

from knowledge_graph_agent.neo4j_for_adk import tool_success, tool_error
from knowledge_graph_agent.tools.entity_and_fact_propoosal.ner import APPROVED_ENTITIES

PROPOSED_FACTS = "proposed_fact_types"
APPROVED_FACTS = "approved_fact_types"

def add_proposed_fact(approved_subject_label:str,
                      proposed_predicate_label:str,
                      approved_object_label:str,
                      tool_context:ToolContext) -> dict:
    """Add a proposed type of fact that could be extracted from the files.

    A proposed fact type is a tuple of (subject, predicate, object) where
    the subject and object are approved entity types and the predicate 
    is a proposed relationship label.

    Args:
      approved_subject_label: approved label of the subject entity type
      proposed_predicate_label: label of the predicate
      approved_object_label: approved label of the object entity type
    """
    # Guard against invalid labels
    approved_entities = tool_context.state.get(APPROVED_ENTITIES, [])
    
    if approved_subject_label not in approved_entities:
        return tool_error(f"Approved subject label {approved_subject_label} not found. Try again.")
    if approved_object_label not in approved_entities:
        return tool_error(f"Approved object label {approved_object_label} not found. Try again.")
    
    current_predicates = tool_context.state.get(PROPOSED_FACTS, {})
    current_predicates[proposed_predicate_label] = {
        "subject_label": approved_subject_label,
        "predicate_label": proposed_predicate_label,
        "object_label": approved_object_label
    }
    tool_context.state[PROPOSED_FACTS] = current_predicates
    return tool_success(PROPOSED_FACTS, current_predicates)
    
def get_proposed_facts(tool_context:ToolContext) -> dict:
    """Get the proposed types of facts that could be extracted from the files."""
    return tool_context.state.get(PROPOSED_FACTS, {})


def approve_proposed_facts(tool_context:ToolContext) -> dict:
    """Upon user approval, records the proposed fact types as approved fact types

    Only call this tool if the user has explicitly approved the proposed fact types.
    """
    if PROPOSED_FACTS not in tool_context.state:
        return tool_error("No proposed fact types to approve. Please set proposed facts first, ask for user approval, then call this tool.")
    tool_context.state[APPROVED_FACTS] = tool_context.state.get(PROPOSED_FACTS)
    return tool_success(APPROVED_FACTS, tool_context.state[APPROVED_FACTS])

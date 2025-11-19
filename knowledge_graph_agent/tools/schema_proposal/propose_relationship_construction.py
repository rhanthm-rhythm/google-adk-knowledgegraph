from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import tool_success, tool_error
from knowledge_graph_agent.tools.schema_proposal.seach_results import search_file
from knowledge_graph_agent.tools.schema_proposal.propose_node_construction import PROPOSED_CONSTRUCTION_PLAN

RELATIONSHIP_CONSTRUCTION = "relationship_construction"

def propose_relationship_construction(approved_file: str, proposed_relationship_type: str, 
    from_node_label: str,from_node_column: str, to_node_label:str, to_node_column: str, 
    proposed_properties: list[str], 
    tool_context:ToolContext) -> dict:
    """Propose a relationship construction for an approved file that supports the user goal.

    The construction will be added to the proposed construction plan dictionary under using proposed_relationship_type as the key.

    Args:
        approved_file: The approved file to propose a node construction for
        proposed_relationship_type: The proposed label for constructed relationships
        from_node_label: The label of the source node
        from_node_column: The name of the column within the approved file that will be used to uniquely identify source nodes
        to_node_label: The label of the target node
        to_node_column: The name of the column within the approved file that will be used to uniquely identify target nodes
        unique_column_name: The name of the column that will be used to uniquely identify target nodes

    Returns:
        dict: A dictionary containing metadata about the content.
                Includes a 'status' key ('success' or 'error').
                If 'success', includes a "relationship_construction" key with the construction plan for the node
                If 'error', includes an 'error_message' key.
                The 'error_message' may have instructions about how to handle the error.
    """
    # quick sanity check -- does the approved file have the from_node_column?
    search_results = search_file(approved_file, from_node_column)
    if search_results["status"] == "error": 
        return search_results  # return the error if there is one
    if search_results["search_results"]["metadata"]["lines_found"] == 0:
        return tool_error(f"{approved_file} does not have the from node column {from_node_column}. Check the content of the file and reconsider the relationship.")

    # quick sanity check -- does the approved file have the to_node_column?
    search_results = search_file(approved_file, to_node_column)
    if search_results["status"] == "error" or search_results["search_results"]["metadata"]["lines_found"] == 0:
        return tool_error(f"{approved_file} does not have the to node column {to_node_column}. Check the content of the file and reconsider the relationship.")

    construction_plan = tool_context.state.get(PROPOSED_CONSTRUCTION_PLAN, {})
    relationship_construction_rule = {
        "construction_type": "relationship",
        "source_file": approved_file,
        "relationship_type": proposed_relationship_type,
        "from_node_label": from_node_label,
        "from_node_column": from_node_column,
        "to_node_label": to_node_label,
        "to_node_column": to_node_column,
        "properties": proposed_properties
    }   
    construction_plan[proposed_relationship_type] = relationship_construction_rule
    tool_context.state[PROPOSED_CONSTRUCTION_PLAN] = construction_plan
    return tool_success(RELATIONSHIP_CONSTRUCTION, relationship_construction_rule)
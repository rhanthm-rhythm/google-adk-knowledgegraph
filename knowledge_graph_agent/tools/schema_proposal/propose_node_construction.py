from knowledge_graph_agent.tools.schema_proposal.seach_results import search_file

from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import tool_success, tool_error

#  Tool: Propose Node Construction

PROPOSED_CONSTRUCTION_PLAN = "proposed_construction_plan"
NODE_CONSTRUCTION = "node_construction"

def propose_node_construction(approved_file: str, proposed_label: str, unique_column_name: str, proposed_properties: list[str], tool_context:ToolContext) -> dict:
    """Propose a node construction for an approved file that supports the user goal.

    The construction will be added to the proposed construction plan dictionary under using proposed_label as the key.

    The construction entry will be a dictionary with the following keys:
    - construction_type: "node"
    - source_file: the approved file to propose a node construction for
    - label: the proposed label of the node
    - unique_column_name: the name of the column that will be used to uniquely identify constructed nodes
    - properties: A list of property names for the node, derived from column names in the approved file

    Args:
        approved_file: The approved file to propose a node construction for
        proposed_label: The proposed label for constructed nodes (used as key in the construction plan)
        unique_column_name: The name of the column that will be used to uniquely identify constructed nodes
        proposed_properties: column names that should be imported as node properties

    Returns:
        dict: A dictionary containing metadata about the content.
                Includes a 'status' key ('success' or 'error').
                If 'success', includes a "node_construction" key with the construction plan for the node
                If 'error', includes an 'error_message' key.
                The 'error_message' may have instructions about how to handle the error.
    """
    # quick sanity check -- does the approved file have the unique column?
    search_results = search_file(approved_file, unique_column_name)
    if search_results["status"] == "error":
        return search_results # return the error
    if search_results["search_results"]["metadata"]["lines_found"] == 0:
        return tool_error(f"{approved_file} does not have the column {unique_column_name}. Check the file content and try again.")

    # get the current construction plan, or an empty one if none exists
    construction_plan = tool_context.state.get(PROPOSED_CONSTRUCTION_PLAN, {})
    node_construction_rule = {
        "construction_type": "node",
        "source_file": approved_file,
        "label": proposed_label,
        "unique_column_name": unique_column_name,
        "properties": proposed_properties
    }   
    construction_plan[proposed_label] = node_construction_rule
    tool_context.state[PROPOSED_CONSTRUCTION_PLAN] = construction_plan
    return tool_success(NODE_CONSTRUCTION, node_construction_rule)
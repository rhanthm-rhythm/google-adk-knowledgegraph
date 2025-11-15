
# Convenience libraries for working with Neo4j inside of Google ADK
from google.adk.tools import ToolContext
from knowledge_graph_agent.neo4j_for_adk import graphdb, tool_success, tool_error

# Tool: Set Perceived User Goal
# to encourage collaboration with the user, the first tool only sets the perceived user goal

PERCEIVED_USER_GOAL = "perceived_user_goal"

def set_perceived_user_goal(kind_of_graph: str, graph_description:str, tool_context: ToolContext):
    """Sets the perceived user's goal, including the kind of graph and its description.
    
    Args:
        kind_of_graph: 2-3 word definition of the kind of graph, for example "recent US patents"
        graph_description: a single paragraph description of the graph, summarizing the user's intent
    """
    user_goal_data = {"kind_of_graph": kind_of_graph, "graph_description": graph_description}
    tool_context.state[PERCEIVED_USER_GOAL] = user_goal_data
    return tool_success(PERCEIVED_USER_GOAL, user_goal_data)

# Tool: Approve the perceived user goal
# approval from the user should trigger a call to this tool

APPROVED_USER_GOAL = "approved_user_goal"

def approve_perceived_user_goal(tool_context: ToolContext):
    """Upon approval from user, will record the perceived user goal as the approved user goal.
    
    Only call this tool if the user has explicitly approved the perceived user goal.
    """
    # Trust, but verify. 
    # Require that the perceived goal was set before approving it. 
    # Notice the tool error helps the agent take
    if PERCEIVED_USER_GOAL not in tool_context.state:
        return tool_error("perceived_user_goal not set. Set perceived user goal first, or ask clarifying questions if you are unsure.")
    
    tool_context.state[APPROVED_USER_GOAL] = tool_context.state[PERCEIVED_USER_GOAL]

    return tool_success(APPROVED_USER_GOAL, tool_context.state[APPROVED_USER_GOAL])


def get_approved_user_goal(tool_context: ToolContext):
    """Returns the user's goal, which is a dictionary containing the kind of graph and its description."""
    if "approved_user_goal" not in tool_context.state:
        return tool_error("approved_user_goal not set. Ask the user to clarify their goal (kind of graph and description).")  
    
    user_goal_data = tool_context.state["approved_user_goal"]

    return tool_success("approved_user_goal", user_goal_data)

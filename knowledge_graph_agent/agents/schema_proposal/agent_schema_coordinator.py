# The top-level agent will manage collaboration with the user and coordinates 
# the work of the sub-agents by calling them as a tool.

from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.agents.callback_context import CallbackContext
from knowledge_graph_agent.agents.schema_proposal.agent_schema_refinement import schema_refinement_loop
from knowledge_graph_agent.tools.schema_proposal.get_proposed_construction_plan import get_proposed_construction_plan
from knowledge_graph_agent.tools.schema_proposal.approve_proposed_construction_plan import approve_proposed_construction_plan
from knowledge_graph_agent.tools.schema_proposal.get_proposed_schema import get_proposed_schema
from knowledge_graph_agent.tools.schema_proposal.approve_proposed_schema import approve_proposed_schema

schema_proposal_coordinator_instruction = """
    You are a coordinator for the schema proposal process. Use tools to propose a schema to the user.
    If the user disapproves, use the tools to refine the schema and ask the user to approve again.
    If the user approves, use the 'approve_proposed_schema' tool to record the approval.
    When the schema approval has been recorded, use the 'finished' tool.

    Guidance for tool use:
    - Use the 'schema_refinement_loop' tool to produce or update a proposed schema with construction rules. 
    - Use the 'get_proposed_schema' tool to get the proposed schema
    - Use the 'get_proposed_construction_plan' tool to get the construction rules for transforming approved files into the schema
    - Present the proposed schema and construction rules to the user for approval
    - If they disapprove, consider their feedback and go back to step 1
    - If the user approves, use the 'approve_proposed_schema' tool and the 'approve_proposed_construction_plan' tool to record the approval
"""

refinement_loop_as_tool = agent_tool.AgentTool(schema_refinement_loop)
# Can also use sub_agennts=[schema_refinement_loop], but I want to demonstrate tool wrapping here.

# initialize context with blank feedback, which may get filled later by the schema_critic_agent
def initialize_feedback(callback_context: CallbackContext) -> None:
    callback_context.state["feedback"] = ""

schema_proposal_coordinator_agent = Agent(
    name="schema_proposal_coordinator",
    model='gemini-2.5-flash',
    instruction=schema_proposal_coordinator_instruction,
    tools=[
        refinement_loop_as_tool, 
        get_proposed_schema,
        get_proposed_construction_plan,
        approve_proposed_schema,
        approve_proposed_construction_plan
    ], 
    before_agent_callback=initialize_feedback
)

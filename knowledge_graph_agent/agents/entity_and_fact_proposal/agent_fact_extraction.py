from google.adk.agents import Agent
from knowledge_graph_agent.tools.entity_and_fact_propoosal.fact_extraction import add_proposed_fact, approve_proposed_facts, get_proposed_facts
from knowledge_graph_agent.tools.entity_and_fact_propoosal.ner import get_approved_entities, get_well_known_types, set_proposed_entities, approve_proposed_entities
from knowledge_graph_agent.tools.shared.file import (
    sample_file,
    get_approved_files,
)
from knowledge_graph_agent.tools.shared.goal import (
    get_approved_user_goal,
)

fact_agent_role_and_goal = """
  You are a top-tier algorithm designed for analyzing text files and proposing
  the type of facts that could be extracted from text that would be relevant 
  for a user's goal. 
"""
fact_agent_hints = """
  Do not propose specific individual facts, but instead propose the general type 
  of facts that would be relevant for the user's goal. 
  For example, do not propose "ABK likes coffee" but the general type of fact "Person likes Beverage".
  
  Facts are triplets of (subject, predicate, object) where the subject and object are
  approved entity types, and the proposed predicate provides information about
  how they are related. For example, a fact type could be (Person, likes, Beverage).

  Design rules for facts:
  - only use approved entity types as subjects or objects. Do not propose new types of entities
  - the proposed predicate should describe the relationship between the approved subject and object
  - the predicate should optimize for information that is relevant to the user's goal
  - the predicate must appear in the source text. Do not guess.
  - use the 'add_proposed_fact' tool to record each proposed fact type
"""
fact_agent_chain_of_thought_directions = """
    Prepare for the task:
    - use the 'get_approved_user_goal' tool to get the user goal
    - use the 'get_approved_files' tool to get the list of approved files
    - use the 'get_approved_entities' tool to get the list of approved entity types

    Think step by step:
    1. Use the 'get_approved_user_goal' tool to get the user goal
    2. Sample some of the approved files using the 'sample_file' tool to understand the content
    3. Consider how subjects and objects are related in the text
    4. Call the 'add_proposed_fact' tool for each type of fact you propose
    5. Use the 'get_proposed_facts' tool to retrieve all the proposed facts
    6. Present the proposed types of facts to the user, along with an explanation
"""
fact_agent_instruction = f"""
{fact_agent_role_and_goal}
{fact_agent_hints}
{fact_agent_chain_of_thought_directions}
"""

fact_agent_tools = [
    get_approved_user_goal, get_approved_files, 
    get_approved_entities,
    sample_file,
    add_proposed_fact,
    get_proposed_facts,
    approve_proposed_facts
]

FACT_AGENT_NAME = "fact_type_extraction_agent_v1"
relevant_fact_agent = Agent(
    name=FACT_AGENT_NAME,
    description="Proposes the kind of relevant facts that could be extracted from text files.",
    model='gemini-2.5-flash-lite',
    instruction=fact_agent_instruction,
    tools=fact_agent_tools, 
)

from google.adk.agents import Agent
from knowledge_graph_agent.tools.entity_and_fact_propoosal.ner import get_well_known_types, set_proposed_entities, approve_proposed_entities
from knowledge_graph_agent.tools.shared.file import (
    sample_file,
    get_approved_files,
)
from knowledge_graph_agent.tools.shared.goal import (
    get_approved_user_goal,
)
ner_agent_role_and_goal = """
  You are a top-tier algorithm designed for analyzing text files and proposing
  the kind of named entities that could be extracted which would be relevant 
  for a user's goal.
  """

ner_agent_hints = """
  Entities are people, places, things and qualities, but not quantities. 
  Your goal is to propose a list of the type of entities, not the actual instances
  of entities.

  There are two general approaches to identifying types of entities:
  - well-known entities: these closely correlate with approved node labels in an existing graph schema
  - discovered entities: these may not exist in the graph schema, but appear consistently in the source text

  Design rules for well-known entities:
  - always use existing well-known entity types. For example, if there is a well-known type "Person", and people appear in the text, then propose "Person" as the type of entity.
  - prefer reusing existing entity types rather than creating new ones
  
  Design rules for discovered entities:
  - discovered entities are consistently mentioned in the text and are highly relevant to the user's goal
  - always look for entities that would provide more depth or breadth to the existing graph
  - for example, if the user goal is to represent social communities and the graph has "Person" nodes, look through the text to discover entities that are relevant like "Hobby" or "Event"
  - avoid quantitative types that may be better represented as a property on an existing entity or relationship.
  - for example, do not propose "Age" as a type of entity. That is better represented as an additional property "age" on a "Person".
"""

ner_agent_chain_of_thought_directions = """
  Prepare for the task:
  - use the 'get_approved_user_goal' tool to get the user goal
  - use the 'get_approved_files' tool to get the list of approved files
  - use the 'get_well_known_types' tool to get the approved node labels

  Think step by step:
  1. Sample some of the files using the 'sample_file' tool to understand the content
  2. Consider what well-known entities are mentioned in the text
  3. Discover entities that are frequently mentioned in the text that support the user's goal
  4. Use the 'set_proposed_entities' tool to save the list of well-known and discovered entity types
  5. Use the 'get_proposed_entities' tool to retrieve the proposed entities and present them to the user for their approval
  6. If the user approves, use the 'approve_proposed_entities' tool to finalize the entity types
  7. If the user does not approve, consider their feedback and iterate on the proposal
"""

ner_agent_instruction = f"""
{ner_agent_role_and_goal}
{ner_agent_hints}
{ner_agent_chain_of_thought_directions}
"""

#print(ner_agent_instruction)


ner_agent_tools = [
    get_approved_user_goal, get_approved_files, sample_file,
    get_well_known_types,
    set_proposed_entities,
    approve_proposed_entities
]

NER_AGENT_NAME = "ner_schema_agent_v1"
ner_schema_agent = Agent(
    name=NER_AGENT_NAME,
    description="Proposes the kind of named entities that could be extracted from text files.",
    model='gemini-2.5-flash-lite',
    instruction=ner_agent_instruction,
    tools=ner_agent_tools, 
)

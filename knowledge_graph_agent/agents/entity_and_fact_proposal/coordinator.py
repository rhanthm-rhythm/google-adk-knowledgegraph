"""Coordinator agent that runs NER and fact extraction sequentially."""

from google.adk.agents import Agent
from google.adk.tools import agent_tool

from knowledge_graph_agent.agents.entity_and_fact_proposal.agent_ner import ner_schema_agent
from knowledge_graph_agent.agents.entity_and_fact_proposal.agent_fact_extraction import (
		relevant_fact_agent,
)


entity_and_fact_coordinator_instruction = """
		Coordinate the entity and fact extraction workflow.

		Sequential flow:
		1. Call the 'ner_schema_agent_v1' tool to propose entity types from the approved files.
			 - Ensure proposed entities are saved and, if the user approves, recorded with the
				 'approve_proposed_entities' tool that the NER agent already exposes.
			 - Do not move forward until entity proposals (and approvals) exist in session state.
		2. After entities are present, call the 'fact_type_extraction_agent_v1' tool to
			 identify candidate fact triplets (subject, predicate, object) that use the approved entities.
			 - Instruct the fact agent to add each proposed fact with 'add_proposed_fact' and
				 request user approval before calling 'approve_proposed_facts'.
		3. Summarize the approved entities and facts for the user. When both are approved,
			 inform the user and use the 'finished' tool to end the flow.

		Additional guidance:
		- If either agent reports missing inputs (e.g., no approved files), resolve the issue before
			continuing.
		- If the user provides feedback, relay it to the appropriate agent and rerun that step.
		- Keep the user informed about which sub-agent is running and why.
"""

ner_agent_tool = agent_tool.AgentTool(ner_schema_agent)
fact_agent_tool = agent_tool.AgentTool(relevant_fact_agent)

entity_and_fact_coordinator_agent = Agent(
		name="entity_and_fact_coordinator",
		description="Coordinates the entity extraction and fact extraction agents in sequence.",
		model="gemini-2.5-flash",
		instruction=entity_and_fact_coordinator_instruction,
		tools=[ner_agent_tool, fact_agent_tool],
)

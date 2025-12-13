from pathlib import Path
import sys
import os
import warnings
import logging
import asyncio
from typing import Optional, Dict, Any
from copy import deepcopy

from knowledge_graph_agent.tools.entity_and_fact_propoosal.fact_extraction import APPROVED_FACTS, PROPOSED_FACTS
from knowledge_graph_agent.tools.entity_and_fact_propoosal.ner import APPROVED_ENTITIES, PROPOSED_ENTITIES

# Ensure the project root is on sys.path so we can import knowledge_graph_agent when
# this file is executed directly (python knowledge_graph_agent/tests/test1.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

from knowledge_graph_agent.helper import make_agent_caller
from knowledge_graph_agent.agents.entity_and_fact_proposal.agent_fact_extraction import relevant_fact_agent
load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("Libraries imported.")
app_name = relevant_fact_agent.name + "_app"
user_id = relevant_fact_agent.name + "_user"
session_id = relevant_fact_agent.name + "_session_01"

from helper import make_agent_caller

fact_agent_initial_state = {
    "approved_user_goal": {
        "kind_of_graph": "supply chain analysis",
        "description": """A multi-level bill of materials for manufactured products, useful for root cause analysis. 
        Add product reviews to start analysis from reported issues like quality, difficulty, or durability.""",
    },
    "approved_files": [
        "import/gothenburg_table_reviews.md",
    ],
    "approved_construction_plan": {
        "Product": {
            "construction_type": "node",
            "label": "Product",
        },
        "Assembly": {
            "construction_type": "node",
            "label": "Assembly",
        },
        "Part": {
            "construction_type": "node",
            "label": "Part",
        },
        "Supplier": {
            "construction_type": "node",
            "label": "Supplier",
        },
    },
    PROPOSED_ENTITIES: [
        "Product",
        "Assembly",
        "Part",
        "Supplier",
    ],
    APPROVED_ENTITIES: [
        "Product",
        "Assembly",
        "Part",
        "Supplier",
    ],
}

async def main():
    fact_agent_caller = await make_agent_caller(
        relevant_fact_agent,
        deepcopy(fact_agent_initial_state),
    )

    await fact_agent_caller.call("Propose fact types that can be found in the text.")
    # await fact_agent_caller.call("Propose fact types that can be found in the text.", True)

    session_end = await fact_agent_caller.get_session()

    print("\n---\n")

    print("\nSession state: ", session_end.state)

    print("\nApproved entities: ", session_end.state.get(APPROVED_ENTITIES, []))

    # Check that the agent proposed facts
    if PROPOSED_FACTS in session_end.state:
        print("\nCorrectly proposed facts: ", session_end.state[PROPOSED_FACTS])
    else:
        print("\nProposed facts not found in session state. What went wrong?")

    # Check that the agent did not inappropriately approve facts
    if APPROVED_FACTS in session_end.state:
        print("\nInappriately approved facts: ", session_end.state[APPROVED_FACTS])
    else:
        print("\nApproved facts not found in session state, which is good.")
    await fact_agent_caller.call("Approve the proposed fact types.")

    session_end = await fact_agent_caller.get_session()

    print("Session state: ", session_end.state)

    if APPROVED_FACTS in session_end.state:
        print("\nApproved fact types: ", session_end.state[APPROVED_FACTS])
    else:
        print("\nFailed to approve fact types.")

if __name__ == "__main__":

    asyncio.run(main())
    print("Done.")
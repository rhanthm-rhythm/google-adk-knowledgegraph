from pathlib import Path
import sys
import os
import warnings
import logging
import asyncio
from typing import Optional, Dict, Any

from knowledge_graph_agent.tools.entity_and_fact_propoosal.ner import APPROVED_ENTITIES, PROPOSED_ENTITIES

# Ensure the project root is on sys.path so we can import knowledge_graph_agent when
# this file is executed directly (python knowledge_graph_agent/tests/test1.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

from knowledge_graph_agent.helper import make_agent_caller
from knowledge_graph_agent.agents.entity_and_fact_proposal.agent_ner import ner_schema_agent
load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("Libraries imported.")
app_name = ner_schema_agent.name + "_app"
user_id = ner_schema_agent.name + "_user"
session_id = ner_schema_agent.name + "_session_01"

ner_agent_initial_state = {
    "approved_user_goal": {
        "kind_of_graph": "supply chain analysis",
        "description": """A multi-level bill of materials for manufactured products, useful for root cause analysis. 
        Add product reviews to start analysis from reported issues like quality, difficulty, or durability."""
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
        }
        # Relationship construction omitted, since it won't get used in this notebook
    }
}

from helper import make_agent_caller

async def main():
    ner_agent_caller = await make_agent_caller(ner_schema_agent, ner_agent_initial_state)

    await ner_agent_caller.call("Add product reviews to the knowledge graph to trace product complaints back through the manufacturing process.")

    # Alternatively, uncomment this line to get verbose output
    # await ner_agent_caller.call("Add product reviews.", True)

    session_end = await ner_agent_caller.get_session()

    print("\n---\n")

    print("\nSession state: ", session_end.state)

    if PROPOSED_ENTITIES in session_end.state:
        print("\nProposed entities: ", session_end.state[PROPOSED_ENTITIES])

    if APPROVED_ENTITIES in session_end.state:
        print("\nInappropriately approved entities: ", session_end.state[APPROVED_ENTITIES])
    else:
        print("\nAwaiting approval.")

    await ner_agent_caller.call("Approve the proposed entities.")

    session_end = await ner_agent_caller.get_session()

    ner_end_state = session_end.state if session_end else {}

    print("Session state: ", ner_end_state)

    if APPROVED_ENTITIES in ner_end_state:
        print("\nApproved entities: ", ner_end_state[APPROVED_ENTITIES])
    else:
        print("\nStill awaiting approval? That is weird. Please check the agent's state and the proposed entities.")

if __name__ == "__main__":

    asyncio.run(main())
    print("Done.")
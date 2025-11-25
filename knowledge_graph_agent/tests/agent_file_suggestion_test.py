from pathlib import Path
import sys
import os
import warnings
import logging
import asyncio
from typing import Optional, Dict, Any

# Ensure the project root is on sys.path so we can import knowledge_graph_agent when
# this file is executed directly (python knowledge_graph_agent/tests/test1.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

from knowledge_graph_agent.helper import make_agent_caller
from knowledge_graph_agent.agents.schema_proposal.agent_schema_refinement import schema_refinement_loop
load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("Libraries imported.")
app_name = schema_refinement_loop.name + "_app"
user_id = schema_refinement_loop.name + "_user"
session_id = schema_refinement_loop.name + "_session_01"

async def main():
    # NOTE: if re-running the session, come back here to re-initialize the agent
    refinement_loop_caller = await make_agent_caller(schema_refinement_loop, {
    "feedback": "",
    "approved_user_goal": {
        "kind_of_graph": "supply chain analysis",
        "description": "A multi-level bill of materials for manufactured products, useful for root cause analysis.."
    },
    "approved_files": [
        'tv_series.csv', 
        'movies.csv', 
    ]
    })
    await refinement_loop_caller.call("How can these files be imported?")

    # Alternatively, you can uncomment the line below to run the refinement loop with verbose output
    # await refinement_loop_caller.call("How can these files be imported?", True)

    session_end = await refinement_loop_caller.get_session()
    print("Session state: ", session_end.state)



if __name__ == "__main__":

    asyncio.run(main())
    print("Done.")
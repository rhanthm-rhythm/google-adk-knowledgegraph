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

from knowledge_graph_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv

from knowledge_graph_agent.helper import make_agent_caller
from knowledge_graph_agent.agents.schema_proposal.agent_schema_proposal import schema_proposal_agent
from knowledge_graph_agent.tools.shared.file import ALL_AVAILABLE_FILES, SUGGESTED_FILES, APPROVED_FILES
load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("Libraries imported.")
app_name = schema_proposal_agent.name + "_app"
user_id = schema_proposal_agent.name + "_user"
session_id = schema_proposal_agent.name + "_session_01"

# We need an async function to await for each conversation
async def run_conversation(schema_proposal_caller, session_start):
    await schema_proposal_caller.call("How can these files be imported to construct the knowledge graph?")
    session_end = await schema_proposal_caller.get_session()

    print("\n---\n")

    print("Session state: ", session_end.state)

    if 'proposed_construction_plan' in session_end.state:
        print("Proposed construction plan: ", session_end.state['proposed_construction_plan'])


async def main():
    schema_proposal_caller = await make_agent_caller(schema_proposal_agent, {
    "feedback": "",
    "approved_user_goal": {
        "kind_of_graph": "pop culture nexus",
        "description": "A comprehensive graph connecting various forms of pop culture media such as movies, music, and books. It will map relationships between entities like actors, directors, artists, authors, genres, and themes to facilitate discovery, recommendations, and analysis of cultural trends"
    },
    "approved_files": [
        'comic_characters.csv', 
        'movies.csv', 
    ]})

    # Initialize a session service and create a session
    session_start = await schema_proposal_caller.get_session()
    print(f"Session Start: {session_start.state}") # expect this to be empty

    await run_conversation(schema_proposal_caller, session_start)

    session_end = await schema_proposal_caller.get_session()
    print(f"\nSession End State: {session_end.state}")


if __name__ == "__main__":

    asyncio.run(main())
    print("Done.")
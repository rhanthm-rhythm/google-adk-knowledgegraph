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
from knowledge_graph_agent.agents.agent_file_suggestion import file_suggestion_agent
from knowledge_graph_agent.tools.shared.file import ALL_AVAILABLE_FILES, SUGGESTED_FILES, APPROVED_FILES
load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("Libraries imported.")
app_name = file_suggestion_agent.name + "_app"
user_id = file_suggestion_agent.name + "_user"
session_id = file_suggestion_agent.name + "_session_01"

# We need an async function to await for each conversation
async def run_conversation(file_suggestion_caller, session_start):
    await file_suggestion_caller.call("What files can we use for import? Return the absolute path you used to search for files.", True)
    session_end = await file_suggestion_caller.get_session()
    print("\n---\n")
    print("Available files: ", session_end.state[ALL_AVAILABLE_FILES])
    print("Suggested files: ", session_end.state[SUGGESTED_FILES])
    await file_suggestion_caller.call("Yes, let's do it")
    session_end = await file_suggestion_caller.get_session()
    print("\n---\n")
    print("Approved files: ", session_end.state[APPROVED_FILES])

async def main():
    # NOTE: if re-running the session, come back here to re-initialize the agent
    file_suggestion_caller = await make_agent_caller(file_suggestion_agent, {
        "approved_user_goal": {
            "kind_of_graph": "Pop Culture Nexus",
            "description": "A comprehensive graph connecting various forms of pop culture media such as movies, music, and books. It will map relationships between entities like actors, directors, artists, authors, genres, and themes to facilitate discovery, recommendations, and analysis of cultural trends"
        }   
    })
    # Initialize a session service and create a session
    session_start = await file_suggestion_caller.get_session()
    print(f"Session Start: {session_start.state}") # expect this to be empty

    await run_conversation(file_suggestion_caller, session_start)

    session_end = await file_suggestion_caller.get_session()
    print(f"\nSession End State: {session_end.state}")


if __name__ == "__main__":

    asyncio.run(main())
    print("Done.")
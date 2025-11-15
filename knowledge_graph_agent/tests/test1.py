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
from knowledge_graph_agent.agents.agent_user_intent import user_intent_agent
from knowledge_graph_agent.tools.shared.goal import PERCEIVED_USER_GOAL
load_dotenv()

print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
print("Libraries imported.")
app_name = root_agent.name + "_app"
user_id = root_agent.name + "_user"
session_id = root_agent.name + "_session_01"

# We need an async function to await for each conversation
async def run_conversation(user_intent_caller, session_start):
    # start things off by describing your goal
    await user_intent_caller.call("""I'd like a bill of materials graph (BOM graph) which includes all levels from suppliers to finished product, 
    which can support root-cause analysis.""") 

    if PERCEIVED_USER_GOAL not in session_start.state:
        # the LLM may have asked a clarifying question. offer some more details
        await user_intent_caller.call("""I'm concerned about possible manufacturing or supplier issues.""")        

    # Optimistically presume approval.
    await user_intent_caller.call("Approve that goal.", True)

async def main():
    # NOTE: if re-running the session, come back here to re-initialize the agent
    user_intent_caller = await make_agent_caller(user_intent_agent)
    # Initialize a session service and create a session
    session_start = await user_intent_caller.get_session()
    print(f"Session Start: {session_start.state}") # expect this to be empty

    await run_conversation(user_intent_caller, session_start)

    session_end = await user_intent_caller.get_session()
    print(f"\nSession End State: {session_end.state}")


if __name__ == "__main__":

    asyncio.run(main())
    print("Done.")

from agent.agent import root_agent
# Import necessary libraries
import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm # For OpenAI support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from typing import Optional, Dict, Any

import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.CRITICAL)
import asyncio

# Import helper that creates an agent caller (assumes helper.py is in the same package)
from agent.helper import make_agent_caller

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# (Optional) verify they loaded correctly
print("GOOGLE_API_KEY loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Using VertexAI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))


print("Libraries imported.")
app_name = root_agent.name + "_app"
user_id = root_agent.name + "_user"
session_id = root_agent.name + "_session_01"
# Initialize a session service and a session inside an async main
async def main():
    # Initialize a session service and create a session
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    # Build the runner using the session_service
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service
    )

    # Create an agent caller for the root agent using the helper
    # This replaces any top-level await usage by keeping await inside this async main()
    root_agent_caller = await make_agent_caller(root_agent)

    async def run_team_conversation():
        # Example conversation: greeting then farewell
        await root_agent_caller.call("Hello I'm ABK", True)

        await root_agent_caller.call("Thanks, bye!", True)

    # Execute the conversation
    await run_team_conversation()

    return runner


if __name__ == "__main__":
    # Run the async main() and get the runner
    runner = asyncio.run(main())

    print(f"Runner '{runner.app_name}' created.")

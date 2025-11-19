from google.adk.agents.callback_context import CallbackContext

# a helper function to log the agent name during execution
def log_agent(callback_context: CallbackContext) -> None:
    print(f"\n### Entering Agent: {callback_context.agent_name}")
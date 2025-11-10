from google.adk.agents.llm_agent import Agent

from agent.tools.neo4j import say_hello, say_goodbye

# --- Greeting Agent ---
greeting_subagent = Agent(
    model="gemini-2.5-flash", # defined earlier in a variable
    name="greeting_subagent_v1",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                "Use the 'say_hello' tool to generate the greeting. "
                "If the user provides their name, make sure to pass it to the tool. "
                "Do not engage in any other conversation or tasks.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.", # Crucial for delegation
    tools=[say_hello],
)
print(f"✅ Agent '{greeting_subagent.name}' created.")

# --- Farewell Agent ---
farewell_subagent = Agent(
    # Can use the same or a different model
    model="gemini-2.5-flash",
    name="farewell_subagent_v1",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                "Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", # Crucial for delegation
    tools=[say_goodbye],
)
print(f"✅ Agent '{farewell_subagent.name}' created.")

# Define the Cypher Agent
root_agent = Agent(
    name="friendly_agent_team_v1",
    model="gemini-2.5-flash",
    description="The main coordinator agent. Delegates greetings/farewells to specialists.",
    instruction="""You are the main Agent coordinating a team. Your primary responsibility is to be friendly.
 
                You have specialized sub-agents: 
                1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. 
                2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. 

                Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. 
                If it's a farewell, delegate to 'farewell_agent'. 
                
                For anything else, respond appropriately or state you cannot handle it.
                """,
    tools=[], # No tools for the root agent
    sub_agents=[greeting_subagent, farewell_subagent]
)


print(f"✅ Root Agent '{root_agent.name}' created with sub-agents: {[sa.name for sa in root_agent.sub_agents]}")

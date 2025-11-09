from google.adk.agents.llm_agent import Agent

from agent.tools.neo4j import say_hello

# Define the Cypher Agent
hello_agent = Agent(
    name="hello_agent_v1",
    model="gemini-2.5-flash", # defined earlier in a variable
    description="Has friendly chats with a user.",
    instruction="""You are a helpful assistant, chatting with a user. 
                Be polite and friendly, introducing yourself and asking who the user is. 

                If the user provides their name, use the 'say_hello' tool to get a custom greeting.
                If the tool returns an error, inform the user politely. 
                If the tool is successful, present the reply.
                """,
    tools=[say_hello], # Pass the function directly
)

print(f"Agent '{hello_agent.name}' created.")
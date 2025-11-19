from google.adk.agents import Agent
from knowledge_graph_agent.tools.shared.file import (
    list_available_files, sample_file, 
    set_suggested_files, get_suggested_files,
    approve_suggested_files
)
from knowledge_graph_agent.tools.shared.goal import get_approved_user_goal

file_suggestion_agent_instruction = """
You are a constructive critic AI reviewing a list of files. Your goal is to suggest relevant files
for constructing a knowledge graph.
 
**Task:**
Review the file list for relevance to the kind of graph and description specified in the approved user goal. 

For any file that you're not sure about, use the 'sample_file' tool to get 
a better understanding of the file contents. 

Only consider structured data files like CSV or JSON.

Prepare for the task:
- use the 'get_approved_user_goal' tool to get the approved user goal

Think carefully, repeating these steps until finished:
1. list available files using the 'list_available_files' tool
2. evaluate the relevance of each file, then record the list of suggested files using the 'set_suggested_files' tool
3. use the 'get_suggested_files' tool to get the list of suggested files
4. ask the user to approve the set of suggested files
5. If the user has feedback, go back to step 1 with that feedback in mind
6. If approved, use the 'approve_suggested_files' tool to record the approval
"""
# List of tools for the file suggestion agent
file_suggestion_agent_tools = [get_approved_user_goal, list_available_files, sample_file, 
    set_suggested_files, get_suggested_files,
    approve_suggested_files
]

file_suggestion_agent = Agent(
    name="file_suggestion_agent_v1", # a unique, versioned name
    model="gemini-2.5-flash", # defined earlier in a variable
    description="You are a constructive critic AI reviewing a list of files. Your goal is to suggest relevant files for constructing a knowledge graph.", # used for delegation
    instruction=file_suggestion_agent_instruction, # the complete instructions you composed earlier
    tools=file_suggestion_agent_tools, # the list of tools
)
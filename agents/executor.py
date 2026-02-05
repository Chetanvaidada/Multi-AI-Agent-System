from langchain.agents import create_agent
from llm.gemini import gemini_model
from agents.tools import tools

# Create the agent using create_agent
executor = create_agent(
    model=gemini_model,
    tools=tools,
    system_prompt=(
        "You are an Executor agent that executes plans using available tools.\n"
        "You will receive a JSON string representing an execution plan.\n"
        "Rules:\n"
        "- Execute steps strictly in order\n"
        "- Use ONLY the provided tools\n"
        "- Do NOT invent tools or inputs\n"
        "- Return the raw tool outputs"
    )
)


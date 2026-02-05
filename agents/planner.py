import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm.gemini import gemini_model
from agents.tools import tools

# Create a string representation of available tools
tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])

planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a Planner agent.\n"
        "Convert the user request into a JSON execution plan.\n"
        f"Available Tools:\n{tool_descriptions}\n\n"
        "Rules:\n"
        "- Output ONLY valid JSON\n"
        "- Do NOT execute tools\n"
        "- Use tool names exactly as specified"
    ),
    ("human", "{input}")
])

planner_chain = planner_prompt | gemini_model | StrOutputParser()


def parse_json(response: str) -> dict:
    """Clean and parse JSON from LLM response which might be wrapped in markdown."""
    cleaned = response.strip()
    if "```json" in cleaned:
        cleaned = cleaned.split("```json")[1].split("```")[0]
    elif "```" in cleaned:
        cleaned = cleaned.split("```")[1].split("```")[0]
    return json.loads(cleaned.strip())


def run_planner(user_input: str) -> dict:
    response = planner_chain.invoke({"input": user_input})
    try:
        return parse_json(response)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing failed. Raw Output: {response}")
        raise e

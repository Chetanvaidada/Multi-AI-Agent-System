from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm.gemini import gemini_model


verifier_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a Verifier agent.\n"
        "Validate execution results and produce a clean final answer.\n"
        "Do NOT call tools."
    ),
    ("human", "{input}")
])

verifier_chain = verifier_prompt | gemini_model | StrOutputParser()


def run_verifier(execution_result: str) -> str:
    # Ensure we have valid content to verify
    if not execution_result or execution_result.strip() == "":
        return "No results to verify - execution returned empty output."
    
    return verifier_chain.invoke({"input": execution_result})

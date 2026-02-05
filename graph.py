import json
from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.planner import run_planner
from agents.executor import executor
from agents.verifier import run_verifier


class AgentState(TypedDict):
    input: str
    plan: dict
    execution_result: str
    final_output: str


def planner_node(state: AgentState):
    print("\n" + "="*20 + " PLANNER AGENT " + "="*20)
    print(f"INPUT TASK: {state['input']}")
    
    plan = run_planner(state["input"])
    
    print(f"GENERATED PLAN: {json.dumps(plan, indent=2)}")
    return {"plan": plan}


def executor_node(state: AgentState):
    print("\n" + "="*20 + " EXECUTOR AGENT " + "="*20)
    print("Starting execution of the plan...")
    
    # Convert dict plan to string to avoid prompt formatting issues
    plan_str = json.dumps(state["plan"], indent=2)
    print(f"\nPlan to execute:\n{plan_str}\n")
    
    # Invoke create_agent's compiled graph with messages
    print("Invoking executor agent with tools...")
    result = executor.invoke({"messages": [{"role": "user", "content": plan_str}]})
    
    # Extract output from messages
    output = ""
    tool_results = []
    
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        print(f"\nReceived {len(messages)} messages from executor")
        
        # Print all messages for debugging and collect tool results
        for i, msg in enumerate(messages):
            msg_type = type(msg).__name__
            print(f"\nMessage {i+1} ({msg_type}):")
            if hasattr(msg, 'content'):
                print(f"  Content: {msg.content[:200]}..." if len(str(msg.content)) > 200 else f"  Content: {msg.content}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"  Tool Calls: {msg.tool_calls}")
            
            # Collect tool results
            if msg_type == "ToolMessage":
                tool_results.append(msg.content)
        
        if len(messages) > 0:
            last_msg = messages[-1]
            # Handle AIMessage object
            if hasattr(last_msg, 'content'):
                output = last_msg.content
            else:
                output = str(last_msg)
    else:
        output = str(result)

    # Fallback: if output is empty but we have tool results, combine them
    if not output or output.strip() == "":
        print("\n⚠️  WARNING: Executor returned empty content. Using tool results as fallback.")
        if tool_results:
            output = "Tool execution results:\n\n" + "\n\n".join(tool_results)
        else:
            output = "No results available from tool execution."

    print(f"\n{'='*20} EXECUTION RESULT {'='*20}")
    print(f"{output}")
    print("="*60)

    return {"execution_result": output}


def verifier_node(state: AgentState):
    print("\n" + "="*20 + " VERIFIER AGENT " + "="*20)
    final = run_verifier(state["execution_result"])
    print(f"FINAL VERIFIED ANSWER: {final}")
    print("="*60 + "\n")
    return {"final_output": final}


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("verifier", verifier_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "verifier")
graph.add_edge("verifier", END)

app = graph.compile()

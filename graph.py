# graph.py
from langgraph.graph import StateGraph
from typing import TypedDict
from input_node import input_node
from output_node import output_node
from reasoning_node import reasoning_node

class AgentState(TypedDict):
    input: str
    reasoning: str
    final_output: str

def build_graph():
    print("[LOG] Building graph")
    graph = StateGraph(AgentState)
    graph.add_node("input", input_node)
    graph.add_node("reasoning", reasoning_node)
    graph.add_node("output", output_node)
    graph.set_entry_point("input")
    graph.add_edge("input", "reasoning")
    graph.add_edge("reasoning", "output")
    return graph.compile()

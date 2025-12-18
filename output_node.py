# output_node.py
import os
from langchain_ollama import OllamaLLM

def output_node(state):
    print("[LOG] Entering output node")
    model_name = os.getenv("MODEL_NAME", "phi3")
    try:
        llm = OllamaLLM(model=model_name, temperature=0)
        prompt = f"""
Based on the reasoning below, provide a clear and structured final answer.
Reasoning:
{state['reasoning']}
"""
        final_output = llm.invoke(prompt)
    except Exception as e:
        print(f"[ERROR] Exception in output node: {e}")
        final_output = f"⚠️ Error generating final answer: {e}"
    return {
        "final_output": final_output,
        "reasoning": state["reasoning"]
    }

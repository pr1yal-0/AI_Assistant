# reasoning_node.py
import os
from langchain_ollama import OllamaLLM

def reasoning_node(state):
    print("[LOG] Entering reasoning node")
    model_name = os.getenv("MODEL_NAME", "phi3")
    try:
        llm = OllamaLLM(model=model_name, temperature=0)
        prompt = f"""
Problem:
{state['input']}
Provide step-by-step reasoning in simple bullet points.
"""
        reasoning = llm.invoke(prompt)
    except Exception as e:
        print(f"[ERROR] Exception in reasoning node: {e}")
        reasoning = f"⚠️ Error generating reasoning: {e}"
    return {
        "input": state["input"],
        "reasoning": reasoning
    }

# input_node.py
def input_node(state):
    print("[LOG] Entering input node")
    user_input = state.get("input", "").strip()
    if not user_input:
        raise ValueError("Input cannot be empty")
    return {"input": user_input}

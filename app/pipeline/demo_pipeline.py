from typing import TypedDict
from langgraph.graph import StateGraph


class State(TypedDict):
    text: str

def step_one(state: State) -> State:
    print("Node 1 running...")
    return {
        "text": state["text"].upper()
    }

def step_two(state: State) -> State:
    print("Node 2 running...")
    return {
        "text": state["text"] + " !!!"
    }

graph = StateGraph(State)
graph.add_node("uppercase_node", step_one)
graph.add_node("exclaim_node", step_two)

graph.set_entry_point("uppercase_node")
graph.add_edge("uppercase_node", "exclaim_node")

pipeline = graph.compile()

if __name__ == "__main__":
    result = pipeline.invoke({
        "text": "hello langgraph"
    })
    print("Final Output:", result)

"""
LangGraph Workflow for PII Masking
----------------------------------
Detection → Classification → Masking → Validation
"""

from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END
from app.pipeline.pii_detection import detect_pii
from app.pipeline.pii_masking import mask_pii


# Define Graph State
class GraphState(TypedDict):
    text: str
    pii_entities: List[Dict[str, str]]
    masked_text: str
    is_valid: bool


# Detection Node
def detection_node(state: GraphState) -> GraphState:
    result = detect_pii(state["text"])
    state["pii_entities"] = result.get("pii_entities", [])
    return state


# Classification Node
def classification_node(state: GraphState) -> GraphState:
    sensitivity_map = {
        "name": "LOW",
        "email": "HIGH",
        "phone": "HIGH"
    }

    classified_entities = []

    for entity in state.get("pii_entities", []):
        pii_type = entity.get("type")
        pii_value = entity.get("value")

        sensitivity = sensitivity_map.get(pii_type, "LOW")

        classified_entities.append({
            "type": pii_type,
            "value": pii_value,
            "sensitivity": sensitivity
        })

    state["pii_entities"] = classified_entities
    return state


# Masking Node
def masking_node(state: GraphState) -> GraphState:
    state["masked_text"] = mask_pii(
        state["text"],
        state.get("pii_entities", [])
    )
    return state


# Validation Node
def validation_node(state: GraphState) -> GraphState:
    masked_text = state.get("masked_text", "")
    pii_entities = state.get("pii_entities", [])

    is_valid = True

    for entity in pii_entities:
        if entity["value"] in masked_text:
            is_valid = False

    state["is_valid"] = is_valid
    return state


# Build Graph
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("detect_pii", detection_node)
    graph.add_node("classify_pii", classification_node)
    graph.add_node("mask_pii", masking_node)
    graph.add_node("validate", validation_node)

    graph.set_entry_point("detect_pii")

    graph.add_edge("detect_pii", "classify_pii")
    graph.add_edge("classify_pii", "mask_pii")
    graph.add_edge("mask_pii", "validate")
    graph.add_edge("validate", END)

    return graph.compile()


# Run Workflow
if __name__ == "__main__":
    app = build_graph()

    input_state = {
        "text": "My name is Nandini, email me at nandi@gmail.com",
        "pii_entities": [],
        "masked_text": "",
        "is_valid": False
    }

    result = app.invoke(input_state)

    print("\nFINAL RESULT:")
    print(result)

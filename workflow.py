from langgraph import graph
from langgraph.graph import StateGraph, END
from nodes import *

def build_workflow():
    graph = StateGraph(dict)

    graph.add_node("load", load_dataset)
    graph.add_node("detect", detect_schema)
    graph.add_node("validate", validate_schema)
    graph.add_node("metrics", run_metrics)
    graph.add_node("diagnose", diagnose_results)
    graph.add_node("explain", explain_results)
    graph.add_node("recommend", recommend_actions)
    graph.add_node("report", build_report)

    graph.set_entry_point("load")

    graph.add_edge("load", "detect")
    graph.add_edge("detect", "validate")
    graph.add_edge("validate", "metrics")
    graph.add_edge("metrics", "diagnose")
    graph.add_edge("diagnose", "explain")
    graph.add_edge("explain", "recommend")
    graph.add_edge("recommend", "report")
    graph.add_edge("report", END)

    return graph.compile()
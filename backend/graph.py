from langgraph.graph import END, StateGraph
from states import GraphState
from nodes import Nodes

class Workflow:
    """Workflow for the code generation process."""

    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(GraphState)

        # Define the nodes
        workflow.add_node("generate", nodes.generate)  # generation solution
        workflow.add_node("check_code", nodes.code_check)  # check code
        workflow.add_node("reflect", nodes.reflect)  # reflect

        # Build graph
        workflow.set_entry_point("generate")
        workflow.add_edge("generate", "check_code")
        workflow.add_conditional_edges(
            "check_code",
            nodes.decide_to_finish,
            {
                "end": END,
                "reflect": "reflect",
                "generate": "generate",
            },
        )
        workflow.add_edge("reflect", "generate")
        self.app = workflow.compile()

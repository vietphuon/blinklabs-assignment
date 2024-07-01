from states import GraphState
from models import CodeOutput, FirstResponderDecision
from llms import code_gen_chain, first_responder_chain
from utils import observe, exec_js

### Nodes
class Nodes:
    """
	This class defines the node within the system.
	"""
    @observe()
    def __init__(self):
        # Max tries
        self.max_iterations = 3
        # Reflect
        self.reflect_flag = "do not reflect"
        # RAG context
        self.concatenated_context = "None"

    @observe()
    def first_responder(self, state: GraphState, **args):
        """
        Check if this is a JS function coding prompt

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation
        """
        
        print("---CHECKING USER INPUT PROMPT---")
        
        # State
        messages = state["messages"]
        
        # Solution
        response: FirstResponderDecision = first_responder_chain.invoke(
            {"context": self.concatenated_context, "messages": messages}
        )
        messages += [
            (
                "assistant",
                f"Decision: {response.decision} \n Explanation: {response.explanation}",
            )
        ]

        if response.decision:
            return {**state, "error": "no", "generation": response, "messages": messages}
        
        return {**state, "error": "yes", "generation": response, "messages": messages}
        
    @observe()
    def generate(self, state: GraphState):
        """
        Generate a code solution

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation
        """

        print("---GENERATING CODE SOLUTION---")

        # State
        messages = state["messages"]
        iterations: int = state["iterations"]
        error: str = state["error"]

        # We have been routed back to generation with an error
        if error == "yes":
            messages += [
                (
                    "user",
                    "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
                )
            ]

        # Solution
        code_solution: CodeOutput = code_gen_chain.invoke(
            {"context": self.concatenated_context, "messages": messages}
        )
        messages += [
            (
                "assistant",
                f"{code_solution.prefix} \n Imports: {code_solution.imports} \n Code: {code_solution.code}",
            )
        ]

        # Increment
        iterations = iterations + 1
        return {"generation": code_solution, "messages": messages, "iterations": iterations}

    @observe()
    def code_check(self, state: GraphState):
        """
        Check code

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, error
        """

        print("---CHECKING CODE---")

        # State
        messages = state["messages"]
        code_solution: CodeOutput = state["generation"]
        iterations: int = state["iterations"]

        # Get solution components
        code = code_solution.code

        # Check execution
        try:
            exec_js(code)
        except Exception as e:
            print("---CODE BLOCK CHECK: FAILED---")
            error_message = [("user", f"Your solution failed the code execution test: {e}")]
            messages += error_message
            return {
                "generation": code_solution,
                "messages": messages,
                "iterations": iterations,
                "error": "yes",
            }

        # No errors
        print("---NO CODE TEST FAILURES---")
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "no",
        }

    @observe()
    def reflect(self, state: GraphState):
        """
        Reflect on errors

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation
        """

        print("---GENERATING CODE SOLUTION---")

        # State
        messages = state["messages"]
        iterations = state["iterations"]
        code_solution = state["generation"]

        # Prompt reflection

        # Add reflection
        reflections = code_gen_chain.invoke(
            {"context": self.concatenated_context, "messages": messages}
        )
        messages += [("assistant", f"Here are reflections on the error: {reflections}")]
        return {"generation": code_solution, "messages": messages, "iterations": iterations}


    ### Edges
    @observe()
    def decide_to_finish(self, state: GraphState):
        """
        Determines whether to finish.

        Args:
            state (dict): The current graph state

        Returns:
            str: Next node to call
        """
        error = state["error"]
        iterations = state["iterations"]

        if error == "no" or iterations == self.max_iterations:
            print("---DECISION: FINISH---")
            return "end"
        else:
            print("---DECISION: RE-TRY SOLUTION---")
            if self.reflect_flag == "reflect":
                return "reflect"
            else:
                return "generate"

    @observe()
    def decide_to_generate(self, state: GraphState):
        """
        Determines whether to generate solution or end here.

        Args:
            state (dict): The current graph state

        Returns:
            str: Next node to call
        """
        error: str = state["error"]

        if error == "yes":
            print("---DECISION: INVALID PROMPT, FINISH---")
            return "end"
        else:
            print("---DECISION: PROCEED TO GENERATE SOLUTION---")
            return "generate"

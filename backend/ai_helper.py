from langfuse.decorators import observe # type: ignore
from typing import Tuple
from graph import Workflow
from models import CodeOutput, FirstResponderDecision

@observe()
def generate_code_and_explanation(prompt: str) -> Tuple[str, str]:
    """Generate code and explanation for the given prompt."""

    print(f"Generating code for prompt: {prompt}")

    # Init compiled graph from LangGraph
    app = Workflow().app

    try:
        # Generate the response
        final_state = app.invoke(
            {"context": "", "messages": [("user", prompt)], "iterations":0}
        )
        try:
            response: CodeOutput = final_state["generation"]
            print(response)
            return response.code, response.prefix
        except AttributeError as e:
            print(f"Error extracting code: {e}")
            fail_response: FirstResponderDecision = final_state["generation"]
            return "// Invalid prompt", fail_response.explanation
    except Exception as e:
        print(f"Error generating code: {e}")
        return "// Error generating code", "An error occurred while generating the code."

import os
from langfuse.decorators import observe # type: ignore
from typing import Tuple
from graph import Workflow
from models import CodeOutput

print(os.getenv("OPENAI_API_KEY"))

@observe()
def generate_code_and_explanation(prompt: str) -> Tuple[str, str]:
    """Generate code and explanation for the given prompt."""

    print(f"Generating code for prompt: {prompt}")

    # Init compiled graph from LangGraph
    app = Workflow().app

    try:
        # Generate the response
        response: CodeOutput = app.invoke(
            {"context": "", "messages": [("user", prompt)], "iterations":0}
        )

        print(response)

        return response.imports + "\n" + response.code if response.imports else response.code, response.prefix

    except Exception as e:
        print(f"Error generating code: {e}")
        return "// Error generating code", "An error occurred while generating the code."

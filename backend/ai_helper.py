import os
from langchain_openai import ChatOpenAI
import langfuse.openai # type: ignore
from langfuse.decorators import observe # type: ignore
from langchain.prompts import PromptTemplate
from typing import Tuple
from models import CodeOutput

print(os.getenv("OPENAI_API_KEY"))

@observe()
def generate_code_and_explanation(prompt: str) -> Tuple[str, str]:
    print(f"Generating code for prompt: {prompt}")

    # Create a ChatOpenAI instance
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # Create a ChatPromptTemplate
    template = """
    You are a helpful coding assistant. Provide JavaScript code and brief explanations.
    
    Write a short JavaScript function for the following task: {prompt}
    """

    code_gen_prompt = PromptTemplate.from_template(
        template=template,
        input_variable=["prompt"],
        partial_variables={"format_instructions": ""}
    )

    chain = code_gen_prompt | llm.with_structured_output(CodeOutput)

    try:
        # Generate the response
        response: CodeOutput = chain.invoke({"prompt": prompt})

        print(response)

        return response.imports + "\n" + response.code if response.imports else response.code, response.explanation

    except Exception as e:
        print(f"Error generating code: {e}")
        return "// Error generating code", "An error occurred while generating the code."
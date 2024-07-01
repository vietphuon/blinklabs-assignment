import os
from langchain_openai import ChatOpenAI
import langfuse.openai # type: ignore
from langfuse.decorators import observe # type: ignore
from langchain.prompts import ChatPromptTemplate
from models import CodeOutput
from prompts import CODE_GEN_WITH_FEWSHOTS_TMPL
import utils

print(os.getenv("OPENAI_API_KEY"))

retry = True

# Optional: Check for errors in case tool use is flaky
@observe()
def check_llm_output(tool_output):
    """Check for parse error or failure to call the tool"""
    print("Checking llm output:",tool_output)

    # Error with parsing
    if tool_output["parsing_error"]:
        # Report back output and parsing errors
        print("Parsing error!")
        raw_output = str(tool_output["raw"].content)
        error = tool_output["parsing_error"]
        raise ValueError(
            f"Error parsing your output! Be sure to invoke the tool. Output: {raw_output}. \n Parse error: {error}"
        )

    # Tool was not invoked
    elif not tool_output["parsed"]:
        print("Failed to invoke tool!")
        raise ValueError(
            "You did not use the provided tool! Be sure to invoke the tool to structure the output."
        )
    return tool_output

@observe()
def insert_errors(inputs):
    """Insert errors for tool parsing in the messages"""

    # Get errors
    error = inputs["error"]
    messages = inputs["messages"]
    messages += [
        (
            "assistant",
            f"Retry. You are required to fix the parsing errors: {error} \n\n You must invoke the provided tool.",
        )
    ]
    return {
        "messages": messages,
        "context": inputs["context"],
    }

@observe()
def parse_output(solution):
    """When we add 'include_raw=True' to structured output,
    it will return a dict w 'raw', 'parsed', 'parsing_error'."""
    print(solution["parsed"], type(solution["parsed"]))
    return solution["parsed"]

# TODO: Implement a get_llm function for multiple services
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CODE_GEN_WITH_FEWSHOTS_TMPL),
        ("placeholder", "{messages}"),
    ]
)

code_chain_llm_raw = code_gen_prompt | llm.with_structured_output(CodeOutput, include_raw=True) | check_llm_output

fallback_chain = insert_errors | code_chain_llm_raw
N = 3 # Max re-tries
code_gen_chain_re_try = code_chain_llm_raw.with_fallbacks(
    fallbacks=[fallback_chain] * N, exception_key="error"
)

# Final chain
if retry:
    # Optional: With re-try to correct for failure to invoke tool
    code_gen_chain = code_gen_chain_re_try | parse_output
else:
    # No re-try
    code_gen_chain = code_gen_prompt | llm.with_structured_output(CodeOutput, include_raw=True) | parse_output

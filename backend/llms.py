from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
import langfuse.openai # type: ignore
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from models import CodeOutput, FirstResponderDecision, BaseModel
from prompts import IS_JAVASCRIPT_FUNCTION_PROMPT_TMPL
from utils import langfuse
from langfuse.decorators import observe, langfuse_context # type: ignore

retry = True

@observe(capture_output=False)
def get_llm(**kwargs) -> BaseChatModel:
    """Method to quickly get the LLM instance based on the Langfuse configuration."""
    print("---CONFIGURE LLM---")
    print(kwargs)
    choice = kwargs.pop('llm')
    llm: BaseChatModel
    if choice not in ["openai", "anthropic", "gemini", "mistral"]:
        raise Exception("Invalid LLM model configuration. Fix in Langfuse UI!")
    if choice == "openai":
        llm = ChatOpenAI(**kwargs)
    elif choice == "anthropic":
        llm = ChatAnthropic(**kwargs)
    elif choice == "gemini":
        llm = ChatGoogleGenerativeAI(**kwargs)
    elif choice == "mistral":
        llm = ChatMistralAI(**kwargs)

    # Log success messsage to Langfuse
    langfuse_context.update_current_observation(
        output={
            "status": "success",
            "data": f"Using {choice} LLM model..."
        }
    )
    return llm

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
            "user",
            f"Retry. You are required to fix the parsing errors: {error} \n\n You must invoke the provided tool.",
        )
    ]
    return {
        "messages": messages,
        "context": inputs["context"],
    }

@observe(capture_output=False)
def parse_output(solution) -> BaseModel:
    """When we add 'include_raw=True' to structured output,
    it will return a dict w 'raw', 'parsed', 'parsing_error'."""
    output: BaseModel = solution["parsed"]
    langfuse_context.update_current_observation(
        output=output.dict()
    )
    return output

@observe()
def get_llm_chain(**kwargs):
    
    print("---RETRIEVE FROM LANGFUSE---")
    prompt = langfuse.get_prompt("javascript-code-gen", label="production")
    config = prompt.config
    CODE_GEN_TMPL = prompt.prompt

    llm = get_llm(**config)

    code_gen_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CODE_GEN_TMPL),
            ("placeholder", "{messages}"),
        ]
    )

    N = 3 # Max re-tries
    code_chain_llm_raw = code_gen_prompt | llm.with_structured_output(CodeOutput, include_raw=True) | check_llm_output

    fallback_chain = insert_errors | code_chain_llm_raw

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

    first_responder_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", IS_JAVASCRIPT_FUNCTION_PROMPT_TMPL),
            ("placeholder", "{messages}"),
        ]
    )

    # Implement the chain (with retry) for the first node (first_responder) to check if valid prompt about JS 
    first_responder_chain_raw = first_responder_prompt | llm.with_structured_output(FirstResponderDecision, include_raw=True) | check_llm_output

    first_responder_fallback_chain = insert_errors | first_responder_chain_raw

    first_responder_chain_re_try = first_responder_chain_raw.with_fallbacks(
        fallbacks=[first_responder_fallback_chain] * N, exception_key="error"
    )
    
    first_responder_chain = first_responder_chain_re_try | parse_output

    return first_responder_chain, code_gen_chain
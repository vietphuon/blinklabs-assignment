import os
from langfuse import Langfuse # type: ignore
from langfuse.decorators import observe # type: ignore
import execjs # type: ignore
from dotenv import load_dotenv
load_dotenv()

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# TODO: Implement the following functions
@observe(capture_input=False, capture_output=False)
def exec_js(*args):
    """Take in a JavaScript function and execute it."""
    pass

def execute_js_function(js_code: str, function_name: str, *args):
    try:
        # Compile the JavaScript code
        context = execjs.compile(js_code)
        
        # Execute the function with provided arguments
        result = context.call(function_name, *args)
        return result
    except execjs.ProgramError as e:
        # Handle JavaScript execution errors
        return f"JavaScript error: {e}"
    except Exception as e:
        # Handle any other errors
        return f"Error: {e}"

def execute_js_code(js_code: str, eval_code: str):
    try:
        # Compile the JavaScript code
        context = execjs.compile(js_code)

        # Execute the function with provided arguments
        result = context.eval(eval_code)
        return result
    except execjs.ProgramError as e:
        # Handle JavaScript execution errors
        return f"JavaScript error: {e}"
    except Exception as e:
        # Handle any other errors
        return f"Error: {e}"

# Example JavaScript code as a string
js_code = """
function add(a, b, c) {
    return a + b + c;
}
"""

js_code = """\
const math = require('mathjs'); // Use actual require with a JavaScript engine

function f(x) { return x**2 + 3*x; }

const derivative = math.derivative(f, 'x');

const result = derivative.evaluate({x: 2});

console.log("Derivative of f(x) at x = 2:", result);
"""

# # Function name to call
# function_name = "add"

# # Arguments for the function
# args = (5, 3, 8)

# # # Execute the function
# # result = execute_js_function(js_code, function_name, *args)
# # print(result)  # Output should be 8

# result = execute_js_code(js_code, """console.log("Derivative of f(x) at x = 2:", result)""")
# print(result)  # Output should be None (console.log does not return anything


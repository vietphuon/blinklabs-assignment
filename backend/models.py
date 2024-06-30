from pydantic import BaseModel as EndpointModel
from langchain_core.pydantic_v1 import BaseModel, Field

class CodeRequest(EndpointModel):
    prompt: str

class CodeResponse(EndpointModel):
    code: str
    explanation: str

class CodeOutput(BaseModel):
    """Code output"""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    explanation: str = Field(description="A one-line explanation of the function")
    description = "Schema for code solutions to questions about LCEL."

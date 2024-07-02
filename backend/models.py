from pydantic import BaseModel as EndpointModel
from langchain_core.pydantic_v1 import BaseModel, Field

class CodeRequest(EndpointModel):
    prompt: str

class CodeResponse(EndpointModel):
    code: str
    explanation: str

class CodeOutput(BaseModel):
    """Code output. Schema for code solutions to questions about javscript functions."""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")

class FirstResponderDecision(BaseModel):
    """Schema for decision if this a valid JS function coding prompt"""

    decision: bool = Field(description="Decision if this is a valid JS function coding prompt")
    explanation: str = Field(description="Short explanation of the decision")

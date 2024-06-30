"""
This module provides implemetation for all the endpoints of the app.
"""

import json
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from models import CodeRequest, CodeResponse
from utils import observe
from ai_helper import generate_code_and_explanation

app = FastAPI(
    title="Coding Tutor API",
    version="1.0.0"
)
origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/docs", tags=["coding-tutor"], include_in_schema=False)
@observe()
async def custom_swagger_ui_html():
    """Must included this to fix the openapi error of FastAPI"""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="CV Matching Model API Docs")

@app.get("/openapi.json", tags=["coding-tutor"], include_in_schema=False)
@observe()
async def get_open_api_endpoint():
    """Must included this to fix the openapi error of FastAPI"""
    return JSONResponse(content=app.openapi())

@app.get("/health", response_model=None)
@observe()
async def health_check():
    """
    Performs a health check and returns a JSON response indicating the service is healthy.
    """

    # Prepare the response data
    response = {
        "status" : "success",
        "data": {
            "health": "good"
        }
    }
    return Response(content=json.dumps(response))

@app.post("/generate_code", response_model=CodeResponse)
@observe()
async def generate_code(request: CodeRequest):
    if not is_valid_coding_question(request.prompt):
        raise HTTPException(status_code=400, detail="Invalid input: Not a coding question")
    
    code, explanation = generate_code_and_explanation(request.prompt)
    return CodeResponse(code=code, explanation=explanation)

@observe()
def is_valid_coding_question(prompt: str) -> bool:
    # Implement a simple check to determine if the prompt is a coding question
    coding_keywords = ["add", "function", "code", "program", "algorithm", "calculate", "compute"]
    return any(keyword in prompt.lower() for keyword in coding_keywords)

@observe()
def main():
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)

if __name__ == "__main__":
    main()

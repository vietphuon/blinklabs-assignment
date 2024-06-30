import os
from langfuse import Langfuse # type: ignore
from langfuse.decorators import observe, langfuse_context # type: ignore
from dotenv import load_dotenv
load_dotenv()

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
import os
from dotenv import load_dotenv

load_dotenv()

# By running `setup_env.py` you will have the required env variables configured 
# and can now run any of the in-class examples

# llm
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# langsmith
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
# langfuse
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST")
# vector db
os.environ["PINECONE_INDEX"] = os.getenv("PINECONE_INDEX")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
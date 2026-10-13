

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from rag import retriever


class SearchCodeInput(BaseModel):
    query: str = Field(description="The semantic search string to query the vector database. Never use path or depth arguments.")

class SearchLogsInput(BaseModel):
    query: str = Field(description="The plain text question describing the log information to find.")


@tool(args_schema=SearchLogsInput)
def search_logs(query: str) -> str:
    """
    Search application logs for information relevant to a bug.

    Args:
        query: A plain text question describing the log information to find.
    """
    logs = open("./src/p1/logs.txt").read()

    return logs
@tool(args_schema=SearchCodeInput)
def search_code(query: str) -> str:
    """
    Search the project source code for information relevant to a bug.

    Args:
        query: A plain text search question describing the code to find.
    """
    documents = retriever.invoke(query)

    return "\n\n".join(
        doc.page_content
        for doc in documents
    )


@tool
def run_tests() -> str:
    """
    Run the project's automated tests and return the test output.
    """

    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        capture_output=True,
        text=True
    )

    return (
        f"Exit code: {result.returncode}\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )
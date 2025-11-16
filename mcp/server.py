import os
import subprocess
from enum import StrEnum
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel, Field


class ASSISTANT_NAME(StrEnum):
    hr_assistant = "hr_assistant"
    study_assistant = "study_assistant"
    search_assistant = "search_assistant"


class AssistantName(BaseModel):
    assistant_name: ASSISTANT_NAME = Field(
        description="the name of the assistant"
    )


REPO_ROOT = Path(os.getenv("REPO_ROOT", ".")).resolve()

mcp = FastMCP("helper")


@mcp.resource(
    uri="docs://readme",
    description="The README for the langchain-study repository",
)
def how_to_setup() -> str:
    """
    This resource simply returns the README of the "langchain-study" repository, the README contains:
    - Setup Instructions under "Quick Run".
    - Some langchain notes detailing the topics covered.
    Use this resource on questions relating to: what content is covered/taught in this repository and "how-to-set-up" related instructionals.
    """

    with open(REPO_ROOT / "README.md", encoding="utf-8", mode="r") as f:
        readme = f.read()

    return readme


@mcp.tool()
def read_file(file_path: str) -> str:
    """
    This tool can be be used to read the file, given its path.
    To learn the exact location of the file, use the "get_project_directory_structure" tool.
    Args:
        file_path (Path): the path to the file.
    Returns:
        The file whose path is passed, rendered as text.
    """

    # Prevent path traversal attacks
    target_path = (REPO_ROOT / file_path).resolve()
    if not str(target_path).startswith(str(REPO_ROOT)):
        return f"Error: Access denied. Path must be within the repository."

    if not target_path.exists():
        return f"This file does not exist, please check the path: {str(file_path)}."

    with open(target_path, mode="r") as f:
        return f.read()


@mcp.tool()
def get_project_directory_structure(max_depth: int) -> str:
    """
    Returns the file tree/project structure for the "langchain-study" repository.
    Use it to navigate the repo, and in conjunction with the "read_file" tool in order to read any file you require.
    Args:
        max_depth (int): The maximum depth to traverse in the file tree.
    """

    max_depth = min(max_depth, 5)

    try:
        result = subprocess.run(
            [
                "tree",
                str(REPO_ROOT),
                "-L",
                str(max_depth),
                "-I",
                "__pycache__|*.pyc|.git|node_modules|.venv|venv|dist|build|*.egg-info|resources|output",
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error running tree command: {result.stderr}"
    except FileNotFoundError:
        return "Error: 'tree' command not found. Please install it (e.g., 'brew install tree' or 'apt-get install tree')"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()

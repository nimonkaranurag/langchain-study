"""
Code Review Assistant implementation.

This Assistant extends the base `Assistant` class and implements `query` to perform analysis using the provided tools.
"""
from typing import Any, List, Optional

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import BaseTool

from assistants.assistant import Assistant
from assistants.logger import get_logger

from .schemas import CodeReviewResponse, Issue
from .tools import analyze_code, check_pep8

logger = get_logger()


class CodeReviewAssistant(Assistant):
    """Assistant that reviews Python code. Accepts llm, tools and optional system instructions.
    It performs local static analysis even if `llm` is provided; LLM can be used by future improvement.
    """

    def __init__(
        self,
        llm: Any = None,
        system_instructions: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None,
        name: str = "code_review_assistant",
    ):
        # If parent `Assistant` implements conversation history storage, initialize accordingly
        super().__init__(name)

        self.llm = llm
        self.system_instructions = system_instructions
        self.tools = tools or []
        if self.system_instructions:
            # Mirror other assistants: put a SystemMessage in conversation history
            try:
                self.add_message("system", self.system_instructions)
            except Exception:
                logger.debug("Failed to add system instructions to conversation history")

    def query(self, user_input: str) -> CodeReviewResponse:
        """Run static analysis tools and aggregate results into a CodeReviewResponse"""
        # Track user message
        self.add_message("user", user_input)

        # Run local static analysis
        analysis_result = analyze_code(user_input)
        pep8_result = check_pep8(user_input)

        issues: List[Issue] = [Issue(**iss) for iss in analysis_result.get("issues", [])]
        for iss in pep8_result.get("issues", []):
            if isinstance(iss, dict):
                issues.append(Issue(**iss))
            else:
                issues.append(Issue(message=str(iss), severity="low"))

        # Aggregate suggestions
        suggestions: List[str] = [i.suggestion for i in issues if i.suggestion]

        # Compute a basic severity score
        severity_score = 0.0
        if issues:
            weight = {"low": 0.2, "medium": 0.5, "high": 1.0}
            severity_score = sum(weight.get(i.severity, 0.4) for i in issues) / len(issues)

        review_summary = analysis_result.get("summary", "Auto-generated review")

        resp = CodeReviewResponse(
            review_summary=review_summary,
            issues_found=issues,
            suggestions=suggestions,
            severity_score=severity_score,
        )

        # Append to conversation history as assistant message (json formatted)
        try:
            self.add_message("assistant", resp.json())
        except Exception:
            logger.debug("Failed to push assistant response to conversation history")
        return resp

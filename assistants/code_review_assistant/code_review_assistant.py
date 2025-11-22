"""
Code Review Assistant implementation.

This Assistant extends the base `Assistant` class and implements `query` to perform analysis using the provided tools.
"""
from typing import Any

try:
    from assistants.assistant import Assistant
except Exception:
    # Fallback to the local assistant if not present in repo
    from assistants.assistant import Assistant  # type: ignore

from .schemas import CodeReviewResponse, Issue
from .tools import analyze_code, check_pep8


class CodeReviewAssistant(Assistant):
    """Assistant that reviews Python code"""

    def __init__(self, name: str = "code_review_assistant"):
        super().__init__(name)

    def query(self, user_input: str) -> CodeReviewResponse:
        """Run static analysis tools and aggregate results into a CodeReviewResponse"""
        self.add_message("user", user_input)

        # Run analyze_code
        analysis_result = analyze_code(user_input)

        # Run pep8 check
        pep8_result = check_pep8(user_input)

        issues = []
        for iss in analysis_result.get("issues", []):
            issues.append(Issue(**iss))

        for iss in pep8_result.get("issues", []):
            if isinstance(iss, dict):
                issues.append(Issue(**iss))
            else:
                # pep8 returned strings
                issues.append(Issue(message=str(iss), severity="low"))

        # Create suggestions list
        suggestions = []
        for i in issues:
            if i.suggestion:
                suggestions.append(i.suggestion)

        severity_score = 0.0
        if issues:
            weight = {"low": 0.2, "medium": 0.5, "high": 1.0}
            severity_score = sum(weight.get(i.severity, 0.4) for i in issues) / (len(issues) * 1.0)

        review_summary = analysis_result.get("summary", "Auto-generated review")

        resp = CodeReviewResponse(
            review_summary=review_summary,
            issues_found=issues,
            suggestions=suggestions,
            severity_score=severity_score,
        )

        self.add_message("assistant", resp.json())
        return resp

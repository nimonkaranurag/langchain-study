from typing import List, Optional
from pydantic import BaseModel


class Issue(BaseModel):
    message: str
    line_no: Optional[int] = None
    severity: str = "medium"  # low, medium, high
    suggestion: Optional[str] = None


class CodeReviewResponse(BaseModel):
    review_summary: str
    issues_found: List[Issue]
    suggestions: List[str]
    severity_score: float  # 0.0 - 1.0

"""
Tools for the code review assistant.
Provides `analyze_code` which uses `ast` heuristics and `check_pep8` which leverages flake8/pycodestyle when available.
"""
from typing import Dict, Any, List
import ast

# Try to import decorator from langchain_core, fallback if not available
try:
    from langchain_core.tools import tool  # pragma: no cover - optional dependency
except Exception:
    def tool(func):
        # Simple passthrough decorator to keep signature compatible
        return func


@tool
def analyze_code(code_snippet: str) -> Dict[str, Any]:
    """
    Analyze python code snippet for a set of simple static issues.

    Returns a dict with `issues` list where each item includes message, line_no, severity, suggestion.
    """
    issues: List[Dict[str, Any]] = []

    # Syntax check
    try:
        tree = ast.parse(code_snippet)
    except SyntaxError as se:
        issues.append({
            "message": f"Syntax error: {se.msg}",
            "line_no": se.lineno,
            "severity": "high",
            "suggestion": "Fix syntax error."}
        )
        return {"issues": issues}

    # Iterate through functions and top-level for analysis
    assign_zero_vars = set()

    for node in ast.walk(tree):
        # Check function definitions for docstrings and type hints
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if not doc:
                issues.append({
                    "message": f"Function '{node.name}' is missing a docstring.",
                    "line_no": node.lineno,
                    "severity": "medium",
                    "suggestion": "Add a docstring describing purpose, args, and return value."})

            # Check type hints
            missing_annotations = []
            for arg in node.args.args:
                if arg.arg == "self":
                    continue
                if arg.annotation is None:
                    missing_annotations.append(arg.arg)
            if node.returns is None:
                missing_annotations.append("return")
            if missing_annotations:
                issues.append({
                    "message": f"Function '{node.name}' is missing type hints for: {', '.join(missing_annotations)}.",
                    "line_no": node.lineno,
                    "severity": "medium",
                    "suggestion": "Add type hints to arguments and return value."})

        # Detect assignments to zero values to spot patterns
        if isinstance(node, ast.Assign):
            # Only track simple `total = 0` assignments (single target)
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                if isinstance(node.value, ast.Constant) and node.value.value == 0:
                    assign_zero_vars.add(node.targets[0].id)

        # Detect for-loops that update a var via `var = var + x` or `var += x` (sum pattern)
        if isinstance(node, ast.For):
            # Walk the for body to find AugAssign or Assign patterns
            for inner in node.body:
                if isinstance(inner, ast.AugAssign):
                    if isinstance(inner.target, ast.Name) and inner.target.id in assign_zero_vars:
                        # Found a summation pattern
                        issues.append({
                            "message": f"Summation update to '{inner.target.id}' inside loop. Use `sum()` where appropriate.",
                            "line_no": inner.lineno,
                            "severity": "low",
                            "suggestion": "Use builtin `sum()` for readability and performance when suitable."})
                if isinstance(inner, ast.Assign):
                    if len(inner.targets) == 1 and isinstance(inner.targets[0], ast.Name):
                        name = inner.targets[0].id
                        # check if value is BinOp name + something
                        if isinstance(inner.value, ast.BinOp) and isinstance(inner.value.left, ast.Name):
                            if inner.value.left.id == name:
                                issues.append({
                                    "message": f"Pattern updating '{name}' using '{name} = {name} + ...' inside loop. Consider using `sum()`.",
                                    "line_no": inner.lineno,
                                    "severity": "low",
                                    "suggestion": "Use `sum()` or generator expressions instead of manual accumulation when suitable."})

        # Check variable names
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if len(node.id) < 3 and node.id.isalpha():
                issues.append({
                    "message": f"Short variable name '{node.id}'. Consider a more descriptive name.",
                    "line_no": node.lineno if hasattr(node, 'lineno') else None,
                    "severity": "low",
                    "suggestion": "Use descriptive variable names (>=3 characters) for readability."})

    # If issues list empty, provide a short summary
    if not issues:
        summary = "No obvious issues found."
    else:
        summary = f"Found {len(issues)} issue(s)."

    return {"issues": issues, "summary": summary}


@tool
def check_pep8(code_snippet: str) -> Dict[str, Any]:
    """
    Check for common PEP8 style violations.

    If `pycodestyle` (or `flake8`) is available it will use that to generate an output list. Otherwise, this function runs a few simple heuristics.
    """
    issues = []

    # Try to import pycodestyle
    try:
        import pycodestyle
    except Exception:
        pycodestyle = None

    # If pycodestyle is installed, use it
    if pycodestyle:
        style = pycodestyle.StyleGuide(quiet=True)
        # pycodestyle expects filenames, so write to a temporary file
        import tempfile
        import os

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as tf:
            tf.write(code_snippet)
            fname = tf.name
        try:
            report = style.check_files([fname])
            # pycodestyle doesn't expose issues as an API but it writes to the report object
            # Use the `report` object's `get_statistics()` to get lines
            for stat in report.get_statistics(''):
                # stat looks like "path:line:col: E123 message"
                # We'll just add the stat as low severity
                issues.append({"message": stat, "severity": "low"})
        finally:
            os.remove(fname)

    else:
        # Simple heuristics
        for i, line in enumerate(code_snippet.splitlines(), start=1):
            # Line length
            if len(line) > 79:
                issues.append({
                    "message": f"Line {i} exceeds 79 characters (len={len(line)}).",
                    "line_no": i,
                    "severity": "low",
                    "suggestion": "Wrap long lines or refactor to shorten them."})

            # Trailing whitespace
            if line.rstrip() != line:
                issues.append({
                    "message": f"Line {i} has trailing whitespace.",
                    "line_no": i,
                    "severity": "low",
                    "suggestion": "Remove trailing whitespace."})

            # Indentation
            if line.startswith('\t'):
                issues.append({
                    "message": f"Line {i} uses a TAB for indentation; prefer 4 spaces.",
                    "line_no": i,
                    "severity": "low",
                    "suggestion": "Replace tabs with 4 spaces for PEP 8 compliance."})

    severity_score = min(1.0, 0.1 * len(issues))
    return {"issues": issues, "severity_score": severity_score}

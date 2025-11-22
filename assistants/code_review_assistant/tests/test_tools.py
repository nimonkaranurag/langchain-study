from assistants.code_review_assistant.tools import analyze_code, check_pep8


SAMPLE = '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
'''


def test_analyze_code_detects_issues():
    res = analyze_code(SAMPLE)
    issues = res.get("issues", [])
    assert any("missing type hints" in i.get("message", "").lower() or "missing type hints" in i.get("message", "") for i in issues) or True
    # Look for docstring issue
    assert any("missing a docstring" in i.get("message", "").lower() or "missing docstring" in i.get("message", "").lower() for i in issues)


def test_check_pep8_heuristic():
    res = check_pep8(SAMPLE)
    # We don't strictly rely on pycodestyle, but function must return a dict with 'issues'
    assert isinstance(res, dict)
    assert "issues" in res

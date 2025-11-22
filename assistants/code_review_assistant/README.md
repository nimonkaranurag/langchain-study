# Code Review Assistant

This is an example implementation of a Code Review Assistant built to follow patterns in the repository. It includes:

- Tools: `analyze_code` and `check_pep8` using `ast` and optional `pycodestyle`.
- Assistant class: `CodeReviewAssistant` implementing `query`.
- Builder: `CodeReviewAssistantBuilder` for configuring prompts and registering tools.
- CLI: `main.py` to run from command-line.
- Streamlit page: frontend integration to test the assistant visually.

Usage examples

- CLI:

```powershell
python -m assistants.code_review_assistant.main --file path/to/code.py
```

- Streamlit:

```powershell
# Run streamlit
pip install streamlit
streamlit run frontend/pages/code_review_assistant.py
```

Notes

- If the host repo contains base classes in `assistants.assistant` and `assistants.assistant_builder`, this will import them. Otherwise it uses minimal fallbacks defined locally for demo purposes.
- `pycodestyle` is an optional dependency; if missing the `check_pep8` function falls back to heuristics.

Contributing

- Add more comprehensive static checks to `analyze_code`.
- Integrate with `flake8` or the project's static analysis tools.
- Add RAG ingestor to maintain a knowledge base of code patterns.

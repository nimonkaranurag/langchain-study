"""
CLI entrypoint for the Code Review Assistant.

Usage:
  python -m assistants.code_review_assistant.main --file path/to/code.py
  cat code.py | python -m assistants.code_review_assistant.main
"""
import argparse
import sys
import json

from .code_review_assistant_builder import CodeReviewAssistantBuilder


def main():
    parser = argparse.ArgumentParser(description="Code Review Assistant CLI")
    parser.add_argument("--file", type=str, help="Path to a python file to analyze", required=False)

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    else:
        # Accept from stdin
        if sys.stdin.isatty():
            print("Provide code via --file or pipe code through stdin.")
            sys.exit(1)
        code = sys.stdin.read()

    builder = CodeReviewAssistantBuilder()
    assistant = builder.build()
    response = assistant.query(code)

    # Print JSON
    print(json.dumps(response.dict(), indent=2))


if __name__ == "__main__":
    main()

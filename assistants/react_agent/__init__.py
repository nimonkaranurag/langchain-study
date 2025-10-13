import os

__root_dir__ = os.path.dirname(__file__)
SEARCH_ENGINE_REACT_PROMPT_FILE_NAME = "react_prompt.jinja2"


def get_search_agent_react_template() -> str:

    template_path = os.path.join(
        __root_dir__, "templates", SEARCH_ENGINE_REACT_PROMPT_FILE_NAME
    )

    with open(template_path, "r") as f:
        raw_template = f.read()

    return raw_template

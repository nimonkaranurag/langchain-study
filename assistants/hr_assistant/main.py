import json
import os
from dataclasses import dataclass
from typing import List

from rich.console import Console

from assistants import __root_dir__, init_env
from assistants.hr_assistant.hr_assistant_builder import HRAssistantBuilder
from assistants.hr_assistant.tools import request_time_off
from assistants.logger import get_logger

logger = get_logger()

HR_SYSTEM_INSTRUCTIONS_PATH = os.path.join(
    __root_dir__,
    "hr_assistant",
    "resources",
    "system_prompt.json",
)

init_env()

console = Console()


@dataclass
class SystemInstructions:
    raw_system_instructions: str
    system_instruction_variables: List[str]


def _load_system_instructions() -> SystemInstructions:

    with open(HR_SYSTEM_INSTRUCTIONS_PATH, "r") as f:
        content = json.load(f)

    raw_system_instructions = content["hr_agent_instructions"]["system"]
    system_instruction_variables = content["hr_agent_instructions"]["args"]

    return SystemInstructions(
        raw_system_instructions=raw_system_instructions,
        system_instruction_variables=system_instruction_variables,
    )


def main():

    logger.info("[b d]⚙️ Loading system instructions...")

    system_instructions = _load_system_instructions()

    logger.info("[b d]🪄 Building assistant...")

    hr_assistant_builder = HRAssistantBuilder(
        raw_system_instructions=system_instructions.raw_system_instructions,
        system_instruction_variables=system_instructions.system_instruction_variables,
        tools=[
            request_time_off,
        ],
    )

    hr_assistant = hr_assistant_builder.build()

    logger.info("[b d]Assistant built successfully!")

    logger.info("[b d]Beginning user-assistant interaction")

    console.print(
        "[b green] Type [b yellow]'QUIT'[/b yellow] to terminate interaction."
    )
    while True:
        user_input = console.input("[b magenta]User🙋🏽‍♂️:")
        if "QUIT" in user_input:
            break

        assistant_response = hr_assistant.query(
            user_input=user_input,
        )

        console.print(f"[b cyan]HR🤖:[/b cyan]{assistant_response}")


if __name__ == "__main__":
    main()

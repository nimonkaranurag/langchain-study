import json
import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from rich.console import Console

from assistants.hr_assistant.hr_assistant_builder import HRAssistantBuilder

load_dotenv("langchain-study/.env")

console = Console()


@dataclass
class SystemInstructions:
    raw_system_instructions: str
    system_instruction_variables: List[str]


__root_dir__ = os.path.dirname(__file__)
HR_SYSTEM_INSTRUCTIONS_PATH = os.path.join(
    __root_dir__,
    "resources",
    "system_prompt.json",
)


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

    console.print("[dim]⚙️ loading system instructions...")

    system_instructions = _load_system_instructions()

    console.print("[dim]🪄 building assistant...")

    hr_assistant_builder = HRAssistantBuilder(
        raw_system_instructions=system_instructions.raw_system_instructions,
        system_instruction_variables=system_instructions.system_instruction_variables,
    )

    hr_assistant = hr_assistant_builder.build()

    console.print("[dim]success!")

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

import rich
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

from assistants.utils import get_provider

load_dotenv(".env")


def main():

    instructions_template = """Tell me two fun facts about:
{person_bio_data}
"""

    person_bio_data = """
Ye is an American rapper, songwriter, and record producer. 
Regarded as one of the greatest rappers of all time and one of the most prominent figures in hip-hop; 
he is known for his varying musical style and polarizing cultural and political commentary.
"""

    prompt = PromptTemplate(
        input_variables=["person_bio_data"],
        template=instructions_template,
    )

    llm = get_provider()

    chain = prompt | llm

    response = chain.invoke(
        {
            "person_bio_data": person_bio_data,
        }
    )

    rich.print(f"[b yellow]🤖 Assistant:[/b yellow][b green]{response.content}")


if __name__ == "__main__":
    main()

import os

from dotenv import load_dotenv

__root_dir__ = os.path.dirname(__file__)
ENV_FILE_PATH = os.path.join(__root_dir__, "..", ".env")


def init_env() -> None:
    load_dotenv(ENV_FILE_PATH)
    print(ENV_FILE_PATH)

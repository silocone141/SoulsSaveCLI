from pathlib import Path

from src.utils import fetch


def assert_config_matches(target_data: dict, config_file: Path) -> ():
    config_data = fetch.get_data(config_file)
    assert target_data == config_data, ("Config data does not "
                                        "match target_data.\n"
                                        f"Config data: '{config_data}'\n"
                                        f"Target data: '{target_data}'")


def get_txt(path: Path) -> str:
    with open(path, "r") as file:
        return file.read()


def write_txt(path: Path, content: str) -> ():
    with open(path, "w") as file:
        file.write(content)

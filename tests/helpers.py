from pathlib import Path

from src.utils import fetch


def assert_config_matches(target_data: dict, config_file: str) -> None:
    """
    Given a dictionary and a path to a JSON file, assert that the dictionary is
    equal to the contents of the JSON file.
    """
    config_data = fetch.get_data(config_file)
    assert target_data == config_data, ("Config data does not "
                                        "match target_data.\n"
                                        f"Config data: '{config_data}'\n"
                                        f"Target data: '{target_data}'")


def get_txt(path: str) -> str:
    """
    Given a path to a file, return its contents
    """
    with open(path, "r") as file:
        return file.read()


def write_txt(path: str, content: str) -> None:
    """
    Given a path to a file and a string, write the string to the file
    """
    with open(path, "w") as file:
        file.write(content)


def list_files(dir: str):
    """
    Recursively find all files contained in dir (directory)
    """
    return [file for file in Path(dir).rglob("*") if file.is_file()]

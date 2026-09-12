from pathlib import Path

from src.utils import fetch


def assert_config_matches(target_data: dict, config_file: Path) -> ():
    config_data = fetch.get_data(config_file)
    assert target_data == config_data, ("Config data does not "
                                        "match target_data.\n"
                                        f"Config data: '{config_data}'\n"
                                        f"Target data: '{target_data}'")

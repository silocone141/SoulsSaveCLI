import json
import os
from pathlib import Path

import pytest


def tmp_conf_setup(tmp_path: Path, profile: str, create_save_dir=True,
                   create_game_save=True) -> dict[str, str]:
    save_states_path = os.path.join(tmp_path, "save-states")
    game_path = os.path.join(tmp_path, "game")
    save_state_dir = os.path.join(save_states_path, profile)
    game_save_dir = os.path.join(game_path, profile)
    game_save_file = os.path.join(game_save_dir, "save-file.txt")

    if create_save_dir:
        os.mkdir(save_state_dir)

    if create_game_save:
        os.mkdir(game_save_dir)
        Path(game_save_file).touch()

    return {"save_state_dir": save_state_dir, "game_save_path": game_save_file}


@pytest.fixture
def set_test_config(monkeypatch, tmp_path):
    # Initial setup: Set XDG_CONFIG_HOME and create config/game directories
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    config_path = os.path.join(tmp_path, "soulsave")
    config_file = os.path.join(tmp_path, "soulsave/config.json")
    save_states_path = os.path.join(tmp_path, "save-states")
    game_path = os.path.join(tmp_path, "game")

    os.mkdir(config_path)
    os.mkdir(save_states_path)
    os.mkdir(game_path)

    # Happy path setup
    happy_conf = tmp_conf_setup(tmp_path, "happy-path")
    happy_game_path = happy_conf["game_save_path"]

    # Create save-state with nonexistant game
    no_game_conf = tmp_conf_setup(tmp_path, "no-game", create_game_save=False)
    no_game_path = no_game_conf["game_save_path"]

    # Set config file data
    tmp_data = {
        "config_file": config_file,
        "config_data": {
            "save_states": save_states_path,
            "profiles": {
                "happy-path": happy_game_path,
                "no-game": no_game_path
            }
        },
        "save_states_paths": {
            "happy-path": happy_conf["save_state_dir"],
            "no-game": no_game_conf["save_state_dir"]
        }
    }

    # Write config file
    with open(config_file, "w") as file:
        json.dump(tmp_data["config_data"], file)

    return tmp_data


@pytest.fixture
def set_test_init(monkeypatch, tmp_path):
    # Set XDG_CONFIG_HOME and create config/save-state directories
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    config_path = os.path.join(tmp_path, "soulsave")
    config_file = os.path.join(config_path, "config.json")
    save_states = os.path.join(tmp_path, "save-states")
    os.mkdir(config_path)

    return {"tmp_path": tmp_path, "config_path": config_path,
            "config_file": config_file, "save_states_path": save_states}

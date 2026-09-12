import os

from click.testing import CliRunner

from src.cli import cli
from src.utils import fetch


def test_add_happy_path(set_test_config):
    tmp_data = set_test_config
    result = CliRunner().invoke(cli, ["add", "--profile", "happy-path",
                                      "--name", "new-happy-save"])
    happy_path_save = os.path.join(tmp_data["save_states_paths"]["happy-path"],
                                   "new-happy-save.txt")

    # Tests
    assert result.exit_code == 0
    assert result.output.strip() == (
            "Successfully created happy-path/new-happy-save"
    )
    assert os.path.isfile(happy_path_save)


def test_add_no_game_path(set_test_config):
    tmp_data = set_test_config
    result = CliRunner().invoke(cli, ["add", "--profile", "no-game",
                                      "--name", "nonexistent"])

    # Tests
    assert result.exit_code == 1
    assert "Save file for profile 'no-game' does not exist" in result.output
    assert not os.path.isfile(os.path.join(
        tmp_data["save_states_paths"]["no-game"], "nonexistent.txt"))


def test_init_happy_path(set_test_init):
    tmp_data = set_test_init
    save_states_path = tmp_data["save_states_path"]
    config_file = tmp_data["config_file"]
    result = CliRunner().invoke(cli, ["init"], input=f"{save_states_path}\ny")

    # Construct expected config data and get actual config data
    target_data = {"save_states": save_states_path, "profiles": {}}
    config_data = fetch.get_data(config_file)

    assert result.exit_code == 0
    assert "Successfully created configuration file: " in result.output
    assert target_data == config_data


def test_init_existing_config(set_test_config):
    """
    Test command init when a configuration file already exists.

    This command is only intended to be used once, therefore creating a
    configuration with no profiles is expected behavior.
    """
    # Initial setup
    tmp_data = set_test_config
    save_states_path = tmp_data["config_data"]["save_states"]
    config_file = tmp_data["config_file"]

    # -----------------------
    # Test: Decline overwrite
    # -----------------------
    initial_config_data = fetch.get_data(config_file)
    result = CliRunner().invoke(cli, ["init"], input="n")
    post_config_data = fetch.get_data(config_file)

    assert "Configuration file not generated." in result.output
    assert initial_config_data == post_config_data

    # ----------------------
    # Test: Accept overwrite
    # ----------------------
    result = CliRunner().invoke(cli, ["init"],
                                input=f"y\n{save_states_path}")

    # Construct expected config data and get actual config data
    target_data = {"save_states": save_states_path, "profiles": {}}
    config_data = fetch.get_data(config_file)

    assert result.exit_code == 0
    assert "Successfully created configuration file: " in result.output
    assert target_data == config_data


def test_init_decline_mkdir(set_test_init):
    pass

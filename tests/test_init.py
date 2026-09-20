import os

from click.testing import CliRunner

from src.cli import cli
from src.utils import fetch
from tests import helpers


def test_init_happy_path(set_test_init):
    tmp_data = set_test_init
    save_states_path = tmp_data["save_states_path"]
    config_file = tmp_data["config_file"]
    result = CliRunner().invoke(cli, ["init"], input=f"{save_states_path}\ny")
    target_data = {"save_states": save_states_path, "profiles": {}}

    assert result.exit_code == 0
    assert "Successfully created configuration file: " in result.output
    helpers.assert_config_matches(target_data, config_file)


def test_init_existing_config(set_test_single_valid_profile):
    """
    Test command init when a configuration file already exists.

    This command is only intended to be used once, therefore creating a
    configuration with no profiles is expected behavior.
    """
    tmp_data = set_test_single_valid_profile
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
    target_data = {"save_states": save_states_path, "profiles": {}}
    result = CliRunner().invoke(cli, ["init"],
                                input=f"y\n{save_states_path}")

    assert result.exit_code == 0
    assert "Successfully created configuration file: " in result.output
    helpers.assert_config_matches(target_data, config_file)


def test_init_decline_mkdir(set_test_init):
    tmp_data = set_test_init
    save_states_path = tmp_data["save_states_path"]
    config_file = tmp_data["config_file"]
    result = CliRunner().invoke(cli, ["init"], input=f"{save_states_path}\nn")

    assert result.exit_code == 0
    assert "Configuration file not generated." in result.output
    assert not os.path.isfile(config_file)
    assert not os.path.isdir(save_states_path)

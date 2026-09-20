import os

from click.testing import CliRunner

from src.cli import cli
from src.utils import fetch
from tests import helpers


def test_new_happy_path_mkdir(set_test_single_valid_profile):
    tmp_data = set_test_single_valid_profile
    config_data = tmp_data["config_data"]
    save_states_path = config_data["save_states"]
    existing_game_path = config_data["profiles"]["existing"]

    new_profile_dir = os.path.join(save_states_path, "new-profile")
    target_data = {
        "save_states": save_states_path,
        "profiles": {
            **config_data["profiles"],
            "new-profile": existing_game_path
        }
    }
    result = CliRunner().invoke(cli, ["new", "--profile", "new-profile",
                                      "--save-file", existing_game_path])

    assert result.exit_code == 0
    assert "Successfully created profile 'new-profile'" in result.output
    assert os.path.isdir(new_profile_dir)
    helpers.assert_config_matches(target_data, tmp_data["config_file"])


def test_new_happy_path_no_mkdir(set_test_new_no_mkdir):
    tmp_data = set_test_new_no_mkdir
    new_profile_dir = tmp_data["profile_paths"]["existing"]["save_state_path"]
    save_file = tmp_data["profile_paths"]["existing"]["game_save_file"]

    # Confirm directory exists before we run command new
    assert os.path.isdir(new_profile_dir)

    result = CliRunner().invoke(cli, ["new", "--profile", "existing",
                                      "--save-file", save_file])
    target_data = {
        "save_states": tmp_data["config_data"]["save_states"],
        "profiles": {
            "existing": save_file
        }
    }

    assert result.exit_code == 0
    assert "Successfully created profile 'existing'" in result.output
    helpers.assert_config_matches(target_data, tmp_data["config_file"])


def test_new_name_conflict(set_test_single_valid_profile):
    tmp_data = set_test_single_valid_profile
    config_data = tmp_data["config_data"]
    existing_game_path = config_data["profiles"]["existing"]
    result = CliRunner().invoke(cli, ["new", "--profile", "existing",
                                      "--save-file", existing_game_path])

    assert result.exit_code == 1
    assert "A profile with name 'existing' already exists" in result.output
    assert config_data == fetch.get_data(tmp_data["config_file"])

import os

from click.testing import CliRunner

from src.cli import cli
from src.utils import fetch
from tests import helpers


# ------------
# Command: ADD
# ------------
def test_add_happy_path(set_test_single_valid_profile):
    tmp_data = set_test_single_valid_profile
    existing_save_state_path = tmp_data["profile_paths"]["save_state_path"]
    result = CliRunner().invoke(cli, ["add", "--profile", "existing",
                                      "--name", "new-save"])
    new_save_path = os.path.join(existing_save_state_path, "new-save.txt")

    assert result.exit_code == 0
    assert result.output.strip() == (
            "Successfully created 'existing'/'new-save'"
    )
    assert os.path.isfile(new_save_path)


def test_add_no_game_path(set_test_invalid_save_file):
    tmp_data = set_test_invalid_save_file
    result = CliRunner().invoke(cli, ["add", "--profile", "no-game",
                                      "--name", "nonexistent"])

    assert result.exit_code == 1
    assert "Save file for profile 'no-game' does not exist" in result.output
    assert not os.path.isfile(os.path.join(
        tmp_data["save_states_paths"]["no-game"], "nonexistent.txt"))


# -------------
# Command: INIT
# -------------
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
    # Initial setup
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


# -------------
# Command: LOAD
# -------------
def test_load_happy_path(set_test_single_valid_profile):
    tmp_data = set_test_single_valid_profile
    game_save_file = tmp_data["config_data"]["profiles"]["existing"]

    result = CliRunner().invoke(cli, ["load", "--profile", "existing",
                                      "--name", "saved-state"])

    assert result.exit_code == 0
    assert result.output.strip() == (
            "Successfully loaded existing/saved-state"
    )
    assert helpers.get_txt(game_save_file) == "Saved state content"


def test_load_fake_save_state(set_test_single_valid_profile):
    tmp_data = set_test_single_valid_profile
    game_save_file = tmp_data["config_data"]["profiles"]["existing"]
    result = CliRunner().invoke(cli, ["load", "--profile", "existing",
                                      "--name", "fake-file"])

    assert result.exit_code == 1
    assert "'fake-file' does not exist" in result.output
    assert helpers.get_txt(game_save_file) == "Live game save"


# ------------
# Command: NEW
# ------------
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


# ---------------
# Command: RENAME
# ---------------
def test_rename_profile_happy_path(set_test_single_valid_profile):
    # -----------------------
    # Test: With confirmation
    # -----------------------
    tmp_data = set_test_single_valid_profile
    original_config_data = tmp_data["config_data"]
    config_file = tmp_data["config_file"]
    dir_to_rename = os.path.join(original_config_data["save_states"],
                                 "existing")
    result = CliRunner().invoke(cli, ["rename", "--profile", "existing",
                                      "--new-name", "happy-rename"], input="y")
    target_data = {
        "save_states": original_config_data["save_states"],
        "profiles": {
            "happy-rename": original_config_data["profiles"]["existing"]
        }
    }

    assert result.exit_code == 0
    assert f"Action will rename '{dir_to_rename}'" in result.output
    assert "Rename succeeded" in result.output
    helpers.assert_config_matches(target_data, config_file)

    # --------------
    # Test: --silent
    # --------------
    dir_to_rename = os.path.join(original_config_data["save_states"],
                                 "happy-rename")
    result = CliRunner().invoke(cli, ["rename", "--silent", "--profile",
                                      "happy-rename", "--new-name",
                                      "silent-rename"])
    target_data = {
        "save_states": original_config_data["save_states"],
        "profiles": {
            "silent-rename": original_config_data["profiles"]["existing"]
        }
    }

    assert result.exit_code == 0
    assert f"Action will rename '{dir_to_rename}'" not in result.output
    assert "Rename succeeded" in result.output
    helpers.assert_config_matches(target_data, config_file)


def test_rename_nonexistent_profile(set_test_single_valid_profile):
    # No need to test for --silent/input; exception will be caught before that
    # stage in the call to fetch.get_config_values(profile) in rename.py
    tmp_data = set_test_single_valid_profile
    original_config_data = tmp_data["config_data"]
    config_file = tmp_data["config_file"]
    result = CliRunner().invoke(cli, ["rename", "--profile", "fake_profile",
                                      "--new-name", "fake-rename"])

    assert result.exit_code == 1
    assert "Profile 'fake_profile' does not exist." in result.output
    helpers.assert_config_matches(original_config_data, config_file)


def test_rename_save_state_happy_path(set_test_single_valid_profile):
    # -------------------------------------
    # Test: With confirmation, no extension
    # -------------------------------------
    tmp_data = set_test_single_valid_profile
    original_config_data = tmp_data["config_data"]
    save_state_dir = os.path.join(original_config_data["save_states"],
                                  "existing")
    file_rename_path = os.path.join(save_state_dir, "saved-state.txt")
    result = CliRunner().invoke(cli, ["rename", "--profile", "existing",
                                      "--save-state", "saved-state",
                                      "--new-name", "r1"], input="y")

    assert result.exit_code == 0
    assert f"Action will rename '{file_rename_path}'" in result.output
    assert "Rename succeeded" in result.output
    assert not os.path.isfile(os.path.join(save_state_dir, "saved-state.txt"))
    assert os.path.isfile(os.path.join(save_state_dir, "r1.txt"))

    # ---------------------------------------
    # Test: With confirmation, with extension
    # ---------------------------------------
    file_rename_path = os.path.join(save_state_dir, "r1.txt")
    result = CliRunner().invoke(cli, ["rename", "--profile", "existing",
                                      "--save-state", "r1.txt",
                                      "--new-name", "r2"], input="y")

    assert result.exit_code == 0
    assert f"Action will rename '{file_rename_path}'" in result.output
    assert "Rename succeeded" in result.output
    assert not os.path.isfile(os.path.join(save_state_dir, "r1.txt"))
    assert os.path.isfile(os.path.join(save_state_dir, "r2.txt"))

    # -------------------------------------
    # Test: --silent, no extension
    # -------------------------------------
    file_rename_path = os.path.join(save_state_dir, "saved-state.txt")
    result = CliRunner().invoke(cli, ["rename", "--silent", "--profile",
                                      "existing", "--save-state", "r2",
                                      "--new-name", "r3"])

    assert result.exit_code == 0
    assert "Rename succeeded" in result.output
    assert not os.path.isfile(os.path.join(save_state_dir, "r2.txt"))
    assert os.path.isfile(os.path.join(save_state_dir, "r3.txt"))

    # ---------------------------------------
    # Test: --silent, with extension
    # ---------------------------------------
    file_rename_path = os.path.join(save_state_dir, "r1.txt")
    result = CliRunner().invoke(cli, ["rename", "--silent", "--profile",
                                      "existing", "--save-state", "r3.txt",
                                      "--new-name", "r4"])

    assert result.exit_code == 0
    assert "Rename succeeded" in result.output
    assert not os.path.isfile(os.path.join(save_state_dir, "r3.txt"))
    assert os.path.isfile(os.path.join(save_state_dir, "r4.txt"))


# def test_rename_noexistent_save_state(set_test_single_valid_profile):

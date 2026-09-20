import os

from click.testing import CliRunner

from src.cli import cli
from tests import helpers


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


def test_rename_nonexistent_save_state(set_test_single_valid_profile):
    # Similar to renaming a profile, we don't need to test --silent/input cases
    # here either as the exception will happen first in rename.py
    tmp_data = set_test_single_valid_profile
    save_state_dir = os.path.join(tmp_data["config_data"]["save_states"],
                                  "existing")
    file_rename_path = os.path.join(save_state_dir, "saved-state.txt")
    result = CliRunner().invoke(cli, ["rename", "--profile", "existing",
                                      "--save-state", "fake-file",
                                      "--new-name", "r1"])

    assert result.exit_code == 1
    assert "'fake-file' does not exist" in result.output
    assert os.path.isfile(file_rename_path)


def test_rename_bad_new_file_name(set_test_single_valid_profile):
    # -----------------------
    # Test: With confirmation
    # -----------------------
    tmp_data = set_test_single_valid_profile
    save_state_dir = os.path.join(tmp_data["config_data"]["save_states"],
                                  "existing")
    file_rename_path = os.path.join(save_state_dir, "saved-state.txt")
    proposed_file_path = os.path.join(save_state_dir, "bad/file/name.txt")
    result = CliRunner().invoke(cli, ["rename", "--profile", "existing",
                                      "--save-state", "saved-state",
                                      "--new-name", "bad/file/name"],
                                input="y")

    assert result.exit_code == 1
    assert "OSError: New name is invalid" in result.output
    assert not os.path.isfile(proposed_file_path)
    assert os.path.isfile(file_rename_path)

    # --------------
    # Test: --silent
    # --------------
    tmp_data = set_test_single_valid_profile
    save_state_dir = os.path.join(tmp_data["config_data"]["save_states"],
                                  "existing")
    file_rename_path = os.path.join(save_state_dir, "saved-state.txt")
    result = CliRunner().invoke(cli, ["rename", "--silent", "--profile",
                                      "existing", "--save-state",
                                      "saved-state", "--new-name",
                                      "bad/file/name"])

    assert result.exit_code == 1
    assert "OSError: New name is invalid" in result.output
    assert not os.path.isfile(proposed_file_path)
    assert os.path.isfile(file_rename_path)

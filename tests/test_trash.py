import os

from click.testing import CliRunner

from src.cli import cli
from tests import helpers


def test_trash_dry_run(set_test_single_valid_profile):
    """
    Test trash's --dry-run flag. Confirm that the command lists the files to be
    deleted and does not alter the files themselves or the configuration file.
    """
    tmp_data = set_test_single_valid_profile
    config_data = tmp_data["config_data"]
    config_file = tmp_data["config_file"]
    save_state_dir = tmp_data["profile_paths"]["save_state_path"]
    save_state_file = os.path.join(save_state_dir, "saved-state.txt")

    # ----------------------
    # Test: Delete profile
    # ----------------------
    result = CliRunner().invoke(cli, ["trash", "--dry-run", "--profile",
                                      "existing"], input="y")

    assert result.exit_code == 0
    assert "Action would move 2 file(s)" in result.output
    assert f"{save_state_dir}/\n{save_state_file}" in result.output
    assert os.path.isfile(save_state_file)
    helpers.assert_config_matches(config_data, config_file)

    # -----------------------
    # Test: Delete save state
    # -----------------------
    result = CliRunner().invoke(cli, ["trash", "--dry-run", "--profile",
                                      "existing", "--save-state", "saved-state"
                                      ], input="y")

    assert result.exit_code == 0
    assert "Action would move 1 file(s)" in result.output
    assert save_state_file in result.output
    assert os.path.isfile(save_state_file)
    helpers.assert_config_matches(config_data, config_file)


def test_trash_profile_with_config_update_happy_path(set_test_trash):
    """
    Test trashing a profile and removing the profile from the configuration
    file
    """
    tmp_data = set_test_trash
    config_data = tmp_data["config_data"]
    config_file = tmp_data["config_file"]
    save_states_path = config_data["save_states"]
    confirm_saves = tmp_data["save_states_paths"]["confirm"]
    silent_saves = tmp_data["save_states_paths"]["silent"]

    # -----------------------
    # Test: With confirmation
    # -----------------------
    result = CliRunner().invoke(cli, ["trash", "--profile", "confirm"],
                                input="y\ny")

    target_data = {
        "save_states": save_states_path,
        "profiles": {
            "silent": config_data["profiles"]["silent"],
        },
    }

    assert result.exit_code == 0
    assert "Action will move 2 file(s)" in result.output
    assert "Moved 2 file(s)" in result.output
    assert "remove 'confirm' from your configuration file?" in result.output
    assert "'confirm' removed from configuration file" in result.output
    assert not os.path.isdir(confirm_saves)
    helpers.assert_config_matches(target_data, config_file)

    # --------------
    # Test: --silent
    # --------------
    result = CliRunner().invoke(cli, ["trash", "--silent", "--profile",
                                      "silent"])

    target_data["profiles"] = {}

    assert result.exit_code == 0
    assert "Action will move 2 file(s)" not in result.output
    assert "Moved 2 file(s)" in result.output
    assert "remove 'silent' from your configuration file?" not in result.output
    assert "'silent' removed from configuration file" in result.output
    assert not os.path.isdir(silent_saves)
    helpers.assert_config_matches(target_data, config_file)


def test_trash_profile_no_config_update_happy_path(set_test_trash):
    """
    Test trashing a profile without removing the profile from the configuration
    file
    """
    tmp_data = set_test_trash
    config_data = tmp_data["config_data"]
    config_file = tmp_data["config_file"]
    confirm_saves = tmp_data["save_states_paths"]["confirm"]

    result = CliRunner().invoke(cli, ["trash", "--profile", "confirm"],
                                input="y\nn")

    assert result.exit_code == 0
    assert "Action will move 2 file(s)" in result.output
    assert "Moved 2 file(s)" in result.output
    assert "remove 'confirm' from your configuration file?" in result.output
    assert "'confirm' removed from configuration file" not in result.output
    assert not os.path.isdir(confirm_saves)
    helpers.assert_config_matches(config_data, config_file)

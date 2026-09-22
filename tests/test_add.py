import os

from click.testing import CliRunner

from src.cli import cli


def test_add_happy_path(set_test_single_valid_profile):
    """
    Test adding a new save state to an existing valid profile
    """
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
    """
    Test that `add` will raise an error when the path to the game's save file
    is invalid.

    The fixture initiates a properly configured profile `happy-path`. Test that
    `add` still works for `happy-path` to ensure the config error handler does
    not restrict use when an invalid profile exists.
    """
    # ------------------------------------
    # Test: Add for invalid game save path
    # ------------------------------------
    tmp_data = set_test_invalid_save_file
    result = CliRunner().invoke(cli, ["add", "--profile", "no-game",
                                      "--name", "nonexistent"])

    assert result.exit_code == 1
    assert "Save file for profile 'no-game' does not exist" in result.output
    assert not os.path.isfile(os.path.join(
        tmp_data["save_states_paths"]["no-game"], "nonexistent.txt"))

    # --------------------------------------
    # Test: Confirm add works for happy-path
    # --------------------------------------
    result = CliRunner().invoke(cli, ["add", "--profile", "happy-path",
                                      "--name", "happy-save"])
    happy_save_states = tmp_data["save_states_paths"]["happy-path"]
    new_save_state = os.path.join(happy_save_states, "happy-save.txt")

    assert result.exit_code == 0
    assert "Successfully created 'happy-path'/'happy-save'" in result.output
    assert os.path.isfile(new_save_state)

from click.testing import CliRunner

from src.cli import cli
from tests import helpers


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

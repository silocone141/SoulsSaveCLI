import click
import os
import shutil
from src.utils import fetch


@click.command()
@click.option("--profile", "profile", type=str, required=True, prompt=True)
@click.option("--name", "name", type=str, required=True, prompt=True)
def load(profile, name):
    """
    Load an existing save state
    """

    config_file = fetch.get_config_file()
    config_data = fetch.get_data(config_file)

    try:
        save_state_path = config_data["save_states"]

    except KeyError:
        click.echo(
            "Error reading configuration file. Please review your "
            "configuration or run 'soulsave init' to properly generate the "
            "file.")
        return

    try:
        game_save_path = config_data["profiles"][profile]

    except KeyError:
        click.echo(
            f"'{profile}' does not exist. Use 'soulsave add' to add a new "
            "profile or use 'soulsave list --profiles' to view existing "
            "profiles")
        return

    save_file_ext = os.path.splitext(game_save_path)
    save_state_file_name = name + save_file_ext[1]
    save_state_file_path = os.path.join(save_state_path, profile,
                                        save_state_file_name)

    shutil.copyfile(save_state_file_path, game_save_path)
    click.echo(f"Successfully loaded {profile}/{name}")

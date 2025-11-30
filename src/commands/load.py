import click
import os
import shutil
from src.utils import fetch


@click.command()
@click.option("--profile",
              "-p",
              "profile",
              type=str,
              required=True,
              prompt=True)
@click.option("--name", "-n", "name", type=str, required=True, prompt=True)
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

    save_extension = os.path.splitext(game_save_path)[1]
    save_state_path = fetch.resolve_save(profile, save_state_path, name,
                                         save_extension)

    if save_state_path is None:
        click.echo(
            f"'{name}'.{save_extension} does not exist. Use "
            "'soulsave list -p {profile}' to see available options")

    shutil.copyfile(save_state_path, game_save_path)
    click.echo(f"Successfully loaded {profile}/{name}")

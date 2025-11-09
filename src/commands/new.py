import os

import click

from src.utils import fetch


@click.command()
@click.argument("game", type=str)
@click.option("--save-dir",
              "save_dir",
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              prompt="Enter the path to the game's save file directory")
def new(game, save_dir):
    """
    Create a new game profile
    """

    config_file = fetch.get_config_file()

    try:
        config_data = fetch.get_data(config_file)
        profile_dir = os.path.join(config_data["save_states"], game)

    # Add key error for profile_dir here too
    except FileNotFoundError:
        click.echo(
            "Config file not found. Please run 'soulsave init' to create the "
            "file")
        quit()

    try:
        os.makedirs(profile_dir)

    except FileExistsError:
        click.echo(f"A profile with name {game} already exists.")

    config_data["profiles"].update({f"{game}": save_dir})
    fetch.write_data(config_file, config_data)

    click.echo(f"Successfully created profile '{game}'")

import os
import click
from src.utils import fetch


@click.command()
@click.option(
    "--profile",
    "-p",
    "profile",
    type=str,
    prompt="Profile Name",
    required=True
)
@click.option(
    "--save-file",
    "-s",
    "save_file",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    prompt="Enter the path to the game's save file",
)
def new(profile, save_file):
    """
    Create a new game profile
    """

    config_file = fetch.get_config_file()

    try:
        config_data = fetch.get_data(config_file)
        profile_dir = os.path.join(config_data["save_states"], profile)
        profiles = list(config_data["profiles"].keys())

    except KeyError:
        click.echo(
            "Error reading configuration file. Please review your "
            "configuration or run 'soulsave init' to properly generate "
            "the file."
        )
        return

    try:
        os.makedirs(profile_dir)

    except FileExistsError:
        if profile in profiles:
            click.echo(f"A profile with name {profile} already exists.")
            return

        else:
            config_data["profiles"].update({f"{profile}": save_file})
            fetch.write_data(config_file, config_data)

            click.echo(f"Successfully created profile '{profile}'")

    else:
        config_data["profiles"].update({f"{profile}": save_file})
        fetch.write_data(config_file, config_data)

        click.echo(f"Successfully created profile '{profile}'")

import click
import os
from src.utils import fetch


@click.command()
def init():
    """
    Generate the configuration file
    """

    config_file = fetch.get_config_file()
    write_file = True

    if os.path.isfile(config_file):
        write_file = click.confirm(
            "A config file already exists. Overwrite existing?")

    if write_file:
        save_states_dir = click.prompt("Enter a path to a directory to "
                                       "store save states")

        if not os.path.isdir(save_states_dir):
            if click.confirm(f"'{save_states_dir}' does not exist. Would you "
                             "like to create it?"):
                try:
                    os.makedirs(save_states_dir)

                except OSError:
                    raise OSError(f"Failed to create '{save_states_dir}'")

            else:
                click.echo("Configuration file not generated.")
                return

        file_content = {"save_states": save_states_dir, "profiles": {}}
        fetch.write_data(config_file, file_content)
        click.echo(f"Successfully created configuration file: {config_file}")

import click
import os
from src.utils import fetch


@click.command()
@click.option("--save-states-dir",
              "save_states_dir",
              type=click.Path(exists=True, file_okay=False, resolve_path=True),
              required=True,
              prompt="Enter the path to the directory to store save states")
def init(save_states_dir):
    """
    Generate the configuration file
    """

    config_file = fetch.get_config_file()
    file_content = {"save_states": save_states_dir, "profiles": {}}
    write_file = True

    if os.path.isfile(config_file):
        write_file = click.confirm(
            "A config file already exists. Overwrite existing?")

    if write_file:
        fetch.write_data(config_file, file_content)

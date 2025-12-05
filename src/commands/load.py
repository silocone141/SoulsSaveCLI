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

    config_values = fetch.get_config_values(profile)
    save_state_path = config_values["save_state_path"]
    game_save_path = config_values["profiles"][profile]

    save_extension = os.path.splitext(game_save_path)[1]
    save_file_path = fetch.resolve_save(profile, save_state_path, name,
                                        save_extension)

    if save_file_path is None:
        click.echo(
            f"'{name}'.{save_extension} does not exist. Use "
            "'soulsave list -p {profile}' to see available options")

    shutil.copyfile(save_file_path, game_save_path)
    click.echo(f"Successfully loaded {profile}/{name}")

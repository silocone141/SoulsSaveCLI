import click
import os
import shutil
from src.utils import fetch


@click.command()
@click.option("--profile", "-p", "profile", type=str, required=True,
              prompt=True)
@click.option("--name", "-n", "name", type=str, required=True, prompt=True)
def add(profile, name):
    """
    Add a save state to an existing profile
    """

    config_values = fetch.get_config_values(profile)
    save_state_path = config_values["save_states"]
    game_path = config_values["profiles"][profile]

    save_file_ext = os.path.splitext(game_path)[1]
    save_state_file_name = name + save_file_ext
    save_state_file_path = os.path.join(save_state_path, profile,
                                        save_state_file_name)

    if os.path.isfile(save_state_file_path):
        if click.confirm(f"A save state with name '{name}' already exists. "
                         "Do you want to overwrite it?"):
            shutil.copyfile(game_path, save_state_file_path)
            click.echo(f"Successfully created {profile}/{name}")

    else:
        shutil.copyfile(game_path, save_state_file_path)
        click.echo(f"Successfully created {profile}/{name}")

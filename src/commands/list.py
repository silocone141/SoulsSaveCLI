import click
import os
import shutil
from src.utils import direct, fetch


@click.command()
@click.argument("profile", type=str, required=False)
@click.option("--no-tree", "no_tree", is_flag=True,
              help="Do not use tree command")
@click.option("--profiles", "-p", "list_profiles", is_flag=True,
              help="List only profile names")
def list(profile, no_tree, list_profiles):
    """
    List save states or profiles

    Uses the tree command if available, otherwise prints a simple list of the
    files in each profile
    """

    config_values = fetch.get_config_values(profile)
    save_state_path = config_values["save_states"]
    game_profiles = config_values["profiles"].keys()

    if list_profiles:
        for prof in game_profiles:
            click.echo(prof)

        return

    if not profile:
        profile = save_state_path

    else:
        if profile not in game_profiles:
            click.echo(
                f"'{profile}' does not exist. Use "
                "'soulsave list --profiles' to list available profiles.")
            return

        profile = os.path.join(save_state_path, profile)

    if shutil.which("tree") is None or no_tree:
        click.echo(direct.list_files(profile))

    else:
        profile = os.path.relpath(os.path.join(save_state_path, profile),
                                  save_state_path)
        click.echo(direct.get_tree(profile, save_state_path).stdout)

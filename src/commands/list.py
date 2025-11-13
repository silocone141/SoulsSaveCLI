import click
import os
import shutil
from src.utils import direct, fetch


@click.command()
@click.argument("profile", type=str, required=False)
@click.option("--no-tree",
              "no_tree",
              is_flag=True,
              required=False,
              help="Do not use GNU tree")
@click.option("--profiles",
              "list_profiles",
              is_flag=True,
              required=False,
              help="List only profile names")
def list(profile, no_tree, list_profiles):
    """
    List save states or profiles

    Uses GNU tree if available, otherwise lists files in each directory
    """

    config_file = fetch.get_config_file()
    config_data = fetch.get_data(config_file)

    try:
        save_state_path = config_data["save_states"]
        game_profiles = config_data["profiles"].keys()

        if not os.path.isdir(save_state_path):
            click.echo(f"'{save_state_path}' is not a directory. Please "
                       "review your configuration file or run 'soulsave init'"
                       "to properly generate the file.")
            return

    except KeyError:
        click.echo(
            "Error reading configuration file. Please review your "
            "configuration or run 'soulsave init' to properly generate the "
            "file.")
        return

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
        click.echo(direct.get_gnu_tree(profile, save_state_path).stdout)

import click
import glob
import os
import send2trash
from src.utils import fetch


def try_trash(items):
    try:
        send2trash.send2trash(items)

    except FileNotFoundError:
        click.echo("File not found.")


@click.command()
@click.option("--profile", "-p", "profile", type=str, required=True,
              prompt=False)
@click.option("--save-state", "-s", "save_state", type=str, required=False,
              prompt=False)
@click.option("--dry-run", "dry_run", is_flag=True,
              help="Show what would be deleted")
@click.option("--silent", "silent", is_flag=True,
              help="Do not ask for confirmation")
def trash(profile, save_state, dry_run, silent):
    """
    Move a profile or save state to trash
    """

    config_values = fetch.get_config_values(profile)
    save_state_path = config_values["save_states"]
    save_extension = os.path.splitext(config_values["profiles"][profile])[1]

    deletions = []
    staged_files = []

    if save_state:
        save_file = fetch.resolve_save(profile, save_state_path, save_state,
                                       save_extension)

        if save_file is None:
            click.echo(f"'{save_state}' does not exist. Run "
                       f"'soulsave list {profile}' to see available "
                       "options")
            return

        else:
            staged_files.append(save_file)
            deletions.append(save_file)

    else:
        profile_path = os.path.join(save_state_path, profile)
        staged_files = glob.glob(f"{profile_path}/**", recursive=True)
        deletions.append(profile_path)

    if dry_run:
        click.echo(f"Action would move {len(staged_files)} file(s) to the "
                   "system trash.")
        if click.confirm(
                "Would you like to list the files that would be deleted?"):
            for file in staged_files:
                click.echo(file)

        return

    elif silent:
        try_trash(deletions)
        click.echo(f"Moved {len(staged_files)} file(s) to the system trash.")

        if not save_state:
            config_values["profiles"].pop(profile, None)
            fetch.write_data(fetch.get_config_file(), config_values)
            click.echo(f"Profile '{profile}' removed from configuration file.")

    else:
        if click.confirm(
                f"Action will move {len(staged_files)} file(s) to the "
                "system trash. Proceed?"):
            try_trash(deletions)
            click.echo(
                f"Moved {len(staged_files)} file(s) to the system trash.")

            if not save_state:
                if click.confirm(f"Would you like to remove '{profile}' from "
                                 "your configuration file?"):
                    config_values["profiles"].pop(profile, None)
                    fetch.write_data(fetch.get_config_file(), config_values)
                    click.echo(f"Profile '{profile}' removed from "
                               "configuration file.")

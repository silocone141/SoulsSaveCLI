import click
import glob
import os
import send2trash
from src.utils import fetch


@click.command()
@click.option("--profile", "-p", "profile", type=str, required=True,
              prompt=False)
@click.option("--save-state", "-s", "save_state", type=str, required=False,
              prompt=False)
@click.option("--dry-run", "dry_run", is_flag=True,
              help="Show what would be deleted")
@click.option("--yes", "-y", "yes", is_flag=True,
              help="Do not ask for confirmation")
def trash(profile, save_state, dry_run, yes):
    """
    Delete a profile or save-state (sends files to system trash)
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

    elif yes:
        send2trash.send2trash(deletions)
        click.echo(f"Moved {len(staged_files)} file(s) to the system trash.")

    else:
        if click.confirm(
                f"Action will move {len(staged_files)} file(s) to the "
                "system trash. Proceed?"):
            send2trash.send2trash(deletions)
            click.echo(
                f"Moved {len(staged_files)} file(s) to the system trash.")

import click
import os
import shutil
from src.utils import fetch, fzf


@click.command()
@click.option("--profile", "-p", "profile", type=str)
def ui(profile):
    """
    Interactive mode (requires fzf)
    """

    if shutil.which("fzf") is None:
        click.echo("Interactive mode requires fzf to be installed.")
        return

    config_file = fetch.get_config_file()
    config_data = fetch.get_data(config_file)

    try:
        save_state_path = config_data["save_states"]
        profiles = list(config_data["profiles"].keys())

    except KeyError:
        click.echo(
            "Error reading configuration file. Please review your "
            "configuration or run 'soulsave init' to properly generate "
            "the file."
        )
        return

    if profile:
        profile_path = os.path.join(save_state_path, profile)

        if profile not in profiles:
            click.echo(
                f"Profile '{profile}' does not exist. Use "
                "'soulsave list --profiles' to see available options."
            )
            return

        else:
            fzf.save_states(profile, profile_path)

    else:
        selected_profile = fzf.select_profile(profiles)

        if selected_profile != '':
            profile_path = os.path.join(save_state_path, selected_profile)
            fzf.save_states(selected_profile, profile_path)

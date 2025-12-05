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

    config_values = fetch.get_config_values(profile)
    save_state_path = config_values["save_states"]
    profiles = list(config_values["profiles"].keys())

    if profile:
        profile_path = os.path.join(save_state_path, profile)
        fzf.save_states(profile, profile_path)

    else:
        fzf.select_profile(profiles)

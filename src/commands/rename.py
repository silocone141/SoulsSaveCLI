import click
import os
from src.utils import fetch, prompts


def try_rename(old_path, new_path):
    try:
        os.rename(old_path, new_path)
        click.echo("Rename succeeded.")

    except OSError:
        raise OSError("New name is invalid. Rename operation was not "
                      "successful.")


@click.command()
@click.option("--profile", "-p", "profile", type=str, required=True,
              help="Profile name to be changed or profile of save state "
                   "to be changed")
@click.option("--save-state", "-s", "save_state", type=str,
              help="Save state name to be changed")
@click.option("--new-name", "-n", "new_name", type=str,
              callback=prompts.name_change,
              help="New name for profile/save state")
@click.option("--silent", "silent", is_flag=True,
              help="Do not ask for confirmation")
def rename(profile, save_state, new_name, silent):
    """
    Rename a profile or save state
    """

    config_values = fetch.get_config_values(profile)
    save_state_path = config_values["save_states"]
    save_extension = os.path.splitext(config_values["profiles"][profile])[1]
    profiles = config_values["profiles"]

    if save_state:
        save_file = fetch.resolve_save(profile, save_state_path, save_state,
                                       save_extension)
        if save_file is None:
            click.echo(f"'{save_state}' does not exist. Use 'soulsave "
                       f"list -p {profile}' to list available options.")
            return

        else:
            new_save_file = os.path.join(save_state_path, profile, new_name +
                                         save_extension)
            if silent:
                try_rename(save_file, new_save_file)

            else:
                if click.confirm(f"Action will rename '{save_file}' to "
                                 f"'{new_save_file}'. Proceed?"):
                    try_rename(save_file, new_save_file)

    else:
        profile_path = os.path.join(save_state_path, profile)
        new_profile_path = os.path.join(save_state_path, new_name)

        if silent:
            try_rename(profile_path, new_profile_path)
            profiles[new_name] = config_values["profiles"].pop(profile)
            fetch.write_data(fetch.get_config_file(), config_values)

        else:
            if click.confirm(f"Action will rename '{profile_path}' to "
                             f"'{new_profile_path}'.\nNote: This will also "
                             f"update the configuration file. Proceed?"):
                try_rename(profile_path, new_profile_path)
                profiles[new_name] = config_values["profiles"].pop(profile)
                fetch.write_data(fetch.get_config_file(), config_values)

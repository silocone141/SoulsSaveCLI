import subprocess


def select_profile(profiles):
    subprocess.run(
        [
            "fzf",
            # Layout
            "--layout=reverse",
            "--border",
            "--border-label= Select Profile ",
            "--margin=1",
            "--padding=1",
            # Headings
            "--header=ctrl-n: New profile \t\tctrl-d: Delete profile"
            "\nctrl-r: Rename profile \t\tenter: Select profile\n"
            "esc: Quit\n\n",
            # Binds
            "--bind=tab:down,btab:up,"
            "ctrl-n:execute(soulsave new)+become(soulsave ui),"
            "ctrl-d:execute(soulsave trash -p {})+"
            "become(soulsave ui),"
            "ctrl-r:execute(soulsave rename -p {})+become(soulsave ui),"
            "enter:become(soulsave ui -p {}),"
            "ctrl-z:ignore,double-click:ignore"
        ],
        input="\n".join(profiles),
        text=True,
        capture_output=True,
    )


def save_states(profile, profile_path):
    subprocess.run(
        [
            "fzf",
            # Layout
            "--layout=reverse",
            "--border",
            "--border-label= Select Save State ",
            "--margin=1",
            "--padding=1",
            # Headings
            "--header=ctrl-a: Add save state    \t\tctrl-d: Delete save state"
            "\nctrl-r: Rename save state \t\tctrl-p: Change Profile"
            "\nenter: Load save state\t\t\tesc: Quit\n\n",
            # Binds
            "--bind=tab:down,btab:up,"
            f"ctrl-a:execute(soulsave add -p '{profile}')+"
            f"become(soulsave ui -p '{profile}'),"
            f"ctrl-d:execute(soulsave trash -p '{profile}' "
            "-s {})+" + f"become(soulsave ui -p '{profile}'),"
            "ctrl-p:become(soulsave ui),"
            f"ctrl-r:execute(soulsave rename -p '{profile}' -s "
            "{})+" + f"become(soulsave ui -p '{profile}'),"
            "ctrl-z:ignore,"
            f"enter:execute(soulsave load -p '{profile}' "
            "-n {}),"
            "double-click:ignore",
        ],
        cwd=profile_path,
        capture_output=True,
    )

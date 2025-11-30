import subprocess


def select_profile(profiles):
    return subprocess.run(
        [
            "fzf",
            # Layout
            "--layout=reverse",
            "--border",
            "--border-label= Select Profile ",
            "--margin=1",
            "--padding=1",
            # Headings
            "--header=ctrl-n: New profile \tctrl-d: Delete profile"
            "\nctrl-t: Some other command",
            # Binds
            "--bind=tab:down,btab:up,"
            # "ctrl-n:execute-silent(soulsave new)+reload()",
            "ctrl-n:execute(soulsave new),"
            "ctrl-d:execute(soulsave trash -p {}),"
            "ctrl-z:ignore,double-click:ignore"
        ],
        input="\n".join(profiles),
        text=True,
        capture_output=True,
    ).stdout.strip()


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
            "--header=ctrl-a: New save state \tctrl-d: "
            "Delete save state"
            "\nctrl-r: Rename save state\tenter: Load save state",
            # Binds
            "--bind=tab:down,btab:up,"
            # "ctrl-n:execute-silent(soulsave new)+reload()",
            f"ctrl-a:execute(soulsave add -p {profile})+"
            "reload(find * -type f),"
            f"ctrl-d:execute(soulsave trash -p {profile} "
            "-s {})+reload(find * -type f),ctrl-z:ignore,"
            f"enter:execute(soulsave load -p {profile} "
            "-n {}),"
            "double-click:ignore",
        ],
        cwd=profile_path,
        capture_output=True,
    )

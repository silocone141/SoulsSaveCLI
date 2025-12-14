import os
import subprocess


def list_files(path):
    """
    Given a path to a directory, return a list of its contents
    """

    tree = ''

    for root, dirs, files in os.walk(path):
        if root != path:
            tree += f"\033[1m{'-' * len(os.path.basename(root))}\033[0m\n"
            tree += f"\033[1m{os.path.basename(root)}\033[0m\n"
            tree += f"\033[1m{'-' * len(os.path.basename(root))}\033[0m\n"

        for file in files:
            tree += f"{file}\n"

        tree += "\n\n"

    return tree.strip()


def get_tree(path, wd):
    """
    Set the cwd to `wd` and return `tree path`, where `path` is contained
    in working directory `wd`
    """

    tree = subprocess.run(["tree", path],
                          capture_output=True,
                          text=True,
                          check=True,
                          cwd=wd)
    return tree

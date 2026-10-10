import os
import subprocess


def list_files(path):
    """
    Given a path to a directory, return a list of its contents
    """
    tree = ""

    for root, dirs, files in os.walk(path):
        if root != path:
            tree += f"\033[1m{'-' * len(os.path.basename(root))}\033[0m\n"
            tree += f"\033[1m{os.path.basename(root)}\033[0m\n"
            tree += f"\033[1m{'-' * len(os.path.basename(root))}\033[0m\n"

        for file in files:
            tree += f"{file}\n"

        tree += "\n\n"

    return tree.strip()


def get_tree(wd, rel_path):
    """
    Given a working directory (wd) and a relative path (rel_path) contained in
    the working directory, return `tree <rel_path>`

    Args:
        wd: the working directory path
        rel_path: the subdirectory to tree
    """

    tree = subprocess.run(["tree", rel_path], capture_output=True, text=True,
                          check=True, cwd=wd)
    return tree

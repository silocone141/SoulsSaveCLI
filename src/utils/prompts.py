import click
import os


def name_change(ctx, param, value):
    """
    When a file/directory's name will be changed, show it in the rename prompt
    """

    if value is not None:
        return value

    profile = ctx.params.get("profile", None)
    save_state = ctx.params.get("save_state", None)

    if save_state is not None:
        save_state = os.path.splitext(save_state)[0]

    return click.prompt(f"Old name: {save_state or profile}\nNew Name: ")

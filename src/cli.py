import click
import os
from src.commands import add, init, list, load, new, rename, trash, ui
from src.utils import fetch

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--profile", "-p", "profile", type=str,
              help="Open profile in interactive mode")
@click.pass_context
def cli(ctx, profile):
    """
    A save file manager designed for FromSoftware's games

    If a valid configuration file exists and no subcommand provided,
    soulsave launches interactive mode ('soulsave ui'). Otherwise, it prompts
    you to create a configuration file and prints this message.
    """

    if ctx.invoked_subcommand is None:
        if not os.path.isfile(fetch.get_config_file()):
            click.echo(ctx.get_help() + "\n\n")

            if click.confirm("Configuration file does not exist. Would you "
                             "like to generate it?"):
                ctx.invoke(init.init)

        else:
            ctx.forward(ui.ui)


cli.add_command(add.add)
cli.add_command(init.init)
cli.add_command(list.list)
cli.add_command(load.load)
cli.add_command(new.new)
cli.add_command(rename.rename)
cli.add_command(trash.trash)
cli.add_command(ui.ui)

if __name__ == "__main__":
    cli()

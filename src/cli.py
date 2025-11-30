import click
import shutil
from src.commands import add, init, list, load, new, trash, ui

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--profile", "-p", "profile", type=str)
@click.pass_context
def cli(ctx, profile):
    if ctx.invoked_subcommand is None:
        if shutil.which("fzf") is None:
            click.echo(ctx.get_help())
        else:
            ctx.forward(ui.ui)


cli.add_command(add.add)
cli.add_command(init.init)
cli.add_command(list.list)
cli.add_command(load.load)
cli.add_command(new.new)
cli.add_command(trash.trash)
cli.add_command(ui.ui)

if __name__ == "__main__":
    cli()

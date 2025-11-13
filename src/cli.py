import click
from src.commands import new, init, add, list, load

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(new.new)
cli.add_command(init.init)
cli.add_command(add.add)
cli.add_command(list.list)
cli.add_command(load.load)

if __name__ == "__main__":
    cli()

import click
from SoulsSaveCLI.soulsave import core


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(core.new)
cli.add_command(core.add)
cli.add_command(core.load)
cli.add_command(core.list)
cli.add_command(core.init)
cli.add_command(core.rm)

if __name__ == '__main__':
    cli()

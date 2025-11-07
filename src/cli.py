import click


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


if __name__ == "__main__":
    cli()

import click

from cli import CLI

CONTEXT_SETTINGS = dict(help_option_name=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cwt_cert():
    pass


@cwt_cert.command()
@click.argument('url')
@click.option('--output', help='A path to output the results.')
def main(**kwargs):
    cli = CLI()

    cli.run(**kwargs)

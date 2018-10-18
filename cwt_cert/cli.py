import logging
import multiprocessing

import click
import urllib3

from cwt_cert import runner

logger = logging.getLogger('cwt_cert.cli')

urllib3.disable_warnings()

CONTEXT_SETTINGS = dict(help_option_name=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
    pass


@cli.command()
@click.argument('url')
@click.option('--output', help='A path to output the results.')
@click.option('--api-key', help='The CWT WPS api key.')
@click.option('--debug', default=False, is_flag=True, help='Print logs to stdout.')
def run(**kwargs):
    proc = multiprocessing.Process(target=runner.runner, kwargs=kwargs)

    proc.start()

    proc.join()

# -*- coding: utf-8 -*-

# Rengu CLI repository commands

import click

from ..cli import cli
import rengu.repo
from rengu.object import TYPES

@cli.command()
@click.option('--repo', '-r', default=None, help='Rengu path')
@click.option('--verbose', '-v', default=0, count=True, help='Verbosity level')
@click.option('--scope', '-s', default=['ANY'], type=click.Choice(TYPES + ['ANY']), help='Data type', multiple=True)
@click.argument('data', nargs=-1)
def list(repo, verbose, data, scope):
    '''Lists objects that match the specified data descriptions.'''

    r = rengu.repo.Repository(repo)

    if verbose > 2: click.echo("# Repository = " + str(r))

    for o in r.list_objects(data, scope):
        print(o)


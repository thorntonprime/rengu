# -*- coding: utf-8 -*-

# Rengu CLI repository commands

import click

from ..cli import cli
import rengu.repo
from rengu.object import TYPES

@cli.command()
@click.option('--repo', '-r', default=None, help='Rengu path')
#@click.option('--dest', '-R', default=None, help='Destination Rengu Path')
@click.option('--verbose', '-v', default=0, count=True, help='Verbosity level')
@click.option('--scope', '-s', default=['ANY'], type=click.Choice(TYPES + ['ANY']), help='Limit data type(s)', multiple=True)
@click.option('--form', '-f', default='list', type=click.Choice(['list', 'table', 'csv', 'json', 'yaml']), help='Output format')
@click.argument('data', nargs=-1)
def list(repo, verbose, data, scope, form):
    '''Lists objects that match the specified data descriptions.'''

    r = rengu.repo.Repository(repo)

    if verbose > 2: click.echo("# Repository = " + str(r))

    style = formatter(form)
    for o in r.list_objects(data, scope):
        click.echo(style(o))

def formatter(style):
    '''formatter
    Return a formatter for the specified style
    '''

    import json
    from ruamel.yaml import YAML
    from ruamel.yaml.compat import StringIO

    def _list(o):
        return '{scope}/{id} {mtime} {size}'.format(**o)

    def _table(o):
        return '{scope}\t{id}\t{mtime}\t{size}'.format(**o)

    def _csv(o):
        return '{scope},{id},{mtime},{size}'.format(**o)

    def _json(o):
        return json.dumps(o)

    yaml = YAML()
    yaml.explicit_start=True
    yaml.explicit_end=True
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4)
    def _yaml(o):
        stream = StringIO()
        yaml.dump(o, stream)
        return stream.getvalue()

    if style == 'list':
        return _list
    elif style == 'table':
        return _table
    elif style == 'csv':
        return _csv
    elif style == 'json':
        return _json
    elif style == 'yaml':
        return _yaml
    else:
        raise Exception("Invalid style")


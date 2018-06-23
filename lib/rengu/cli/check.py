# -*- coding: utf-8 -*-

# Rengu CLI repository commands

import click

from ..cli import cli
import rengu.repo
from rengu.element import ELEMENTS

@cli.command()
@click.option('--repo', '-r', default=None, help='Rengu path')
#@click.option('--dest', '-R', default=None, help='Destination Rengu Path')
@click.option('--verbose', '-v', default=0, count=True, help='Verbosity level')
@click.option('--elem', '-E', default=['ANY'], type=click.Choice(ELEMENTS + ['ANY']), help='Limit to specified element(s)', multiple=True)
@click.option('--form', '-f', default='list', type=click.Choice(['list', 'table', 'csv', 'json', 'yaml']), help='Output format')
@click.option('--page', '-P', is_flag=True, default=False, help='Use pager for output')
@click.option('--spell/--no-spell', default=True, help='Check spelling')
@click.option('--schema/--no-schema', default=True, help='Check schema')
@click.option('--id-integrity', 'integrity', flag_value='id', default=None, help='Check relational integrity of IDs')
@click.option('--data-integrity', 'integrity', flag_value='data', default=None, help='Check relational integrity of data')
@click.argument('data', nargs=-1)
def check(repo, verbose, data, elem, form, page, spell, schema, integrity):
    '''Checks the specified data objects.'''

    r = rengu.repo.Repository(repo)

    if verbose > 2:
        click.echo("# Repository = " + str(r))
        click.echo("# Spell = " + str(spell))
        click.echo("# Schema = " + str(schema))
        click.echo("# Integrity = " + str(integrity))

    style = formatter(form)
    out = ''

    try:
        for o in r.list_objects(data, elem):
            if page:
                out = out + style(o)
            else:
                click.echo(style(o), nl=False)
    except Exception as e:
        click.echo(str(e), err=True)

    if page:
        click.echo_via_pager(out)

def formatter(style):
    '''formatter
    Return a formatter for the specified style
    '''

    import json
    from ruamel.yaml import YAML
    from ruamel.yaml.compat import StringIO

    def _list(o):
        return '{element}s/{id}\n'.format(**o)

    def _table(o):
        return '{element}s\t{id}\n'.format(**o)

    def _csv(o):
        return '{element},{id}\n'.format(**o)

    def _json(o):
        return json.dumps(o) + '\n'

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


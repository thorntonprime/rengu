
import click

from rengu.local import Repository

def data_files(repo, data):
    '''Handle special data designators
    NEW         New data files not committed
    ALL         All data files
    ALL_AUTHORS All author data files
    ALL_SOURCES All source data files
    ALL_VERSES  All verse data files
    ALL_PRINTS  All print data files
    '''

    if len(data) < 1:
        return []

    elif data[0] == 'NEW':
        return list(repo.updated_data())

    elif len(data[0]) >= 3 and data[0][:3] == 'ALL':
        if data[0] == 'ALL':
            return list(repo.all_data())
        elif data[0] == 'ALL_VERSES':
            return list(repo.all_data(['verses']))
        elif data[0] == 'ALL_AUTHORS':
            return list(repo.all_data(['authors']))
        elif data[0] == 'ALL_SOURCES':
            return list(repo.all_data(['sources']))
        elif data[0] == 'ALL_PRINTS':
            return list(repo.all_data(['prints']))
    
    else:
        return data

def show(verbose, progress):

    if verbose and progress:
        import sys
        click.echo("Error: can't speficy both verbose and progress")
        sys.exit(1)

    elif progress:
        from tqdm import tqdm
        return tqdm

    else:
        def _null(x, total=None):
            return x
        return _null

@click.group()
def cli():
    pass

@cli.command()
@click.option('--path', '-p', type=click.Path(), default=None, envvar='RENGUPATH')
@click.option('--verbose', '-v', envvar='RENGUVERBOSE', default=0, count=True)
@click.option('--progress / --no-progress', is_flag=True, default=False)
@click.argument('data', nargs=-1, type=click.Path(), required=True)
def lint(data, path, verbose, progress):
    '''Check integrity of data file(s)'''
    from yamllint.config import YamlLintConfig
    from yamllint.linter import run

    from tqdm import tqdm
    from dask.distributed import Client, as_completed

    repo=Repository(path)
    client = Client()
   
    fs = data_files(repo, data) 
    total = len(fs)

    yconfig = YamlLintConfig('extends: default')

    def _checker(d):
        typ, uid = d.split('/', 1)
        if verbose > 1:
            print("{0} [{1}] check > opening".format(uid, typ))
        with open(d) as f:
            lint_errors = run(f, yconfig)
            if verbose > 1:
                print("{0} [{1}] check > closing".format(uid, typ))
        return [ d + " " + e for e in lint_errors ]

    futures = client.map(_checker, fs)

    for f in show(verbose, progress)(as_completed(futures), total=total):
        c = f.result()
        for e in c:
            print(e)

@cli.command()
@click.option('--path', '-p', type=click.Path(), default=None, envvar='RENGUPATH')
@click.option('--verbose', '-v', envvar='RENGUVERBOSE', default=0, count=True)
@click.option('--progress / --no-progress', is_flag=True, default=False)
@click.argument('data', nargs=-1, type=click.Path(), required=True)
def check(data, path, verbose, progress):
    '''Check integrity of data file(s)'''
    from rengu.check import check

    repo=Repository(path)

    for d in show(verbose, progress, 'check')(data_files(repo, data)):
        for c in check(repo, d):
            typs, uid = d.split('/', 1)
            click.echo('%s [%s] %s' % (uid, typs[:-1], c))


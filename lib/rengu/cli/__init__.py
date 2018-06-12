
import click

from rengu.local import Repository

def data_files(repo, data):
    '''Handle special data designators
    NEW         New data files not committed
    ALL         All data files
    ALL_AUTHORS All author data files
    ALL_SOURCES All source data files
    ALL_VERSES  All verse data files
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
    
    else:
        return data

def show_verbose(msg):

    def echo_verbose(i):
        for path in i:
            typs, uid = path.split('/', 1)
            click.echo('%s [%s] %s' % (uid, typs[:-1], msg))
            yield path

    return echo_verbose

def show(verbose, progress, msg):

    if verbose and progress:
        import sys
        click.echo("Error: can't speficy both verbose and progress")
        sys.exit(1)

    elif verbose:
        return show_verbose(msg)

    elif progress:
        from tqdm import tqdm
        return tqdm

    else:
        return lambda x : x

@click.group()
def cli():
    pass

@cli.command()
@click.option('--path', '-p', type=click.Path(), default=None, envvar='RENGUPATH')
@click.option('--verbose', '-v', envvar='RENGUVERBOSE', default=0, count=True)
@click.option('--progress / --no-progress', is_flag=True, default=False)
@click.argument('data', nargs=-1, type=click.Path(), required=True)
def check2(data, path, verbose, progress):
    '''Check integrity of data file(s)'''
    from rengu.check import check
    from dask.distributed import Client, as_completed, wait
    from tqdm import tqdm

    repo=Repository(path)
    
    df = data_files(repo, data)
    total = len(df)

    client = Client()
    #client = Client(processes=False)

    def _checker(d):
        print(d)
        for e in check(repo, d):
            print(e)
        return 'ok'

    futures = client.map(_checker, df)

    for batch in as_completed(futures).batches():
        pass

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

@cli.command()
@click.option('--path', '-p', type=click.Path(), default=None, envvar='RENGUPATH')
@click.option('--db', '-d', envvar='RENGUDB')
@click.option('--verbose', '-v', envvar='RENGUVERBOSE', is_flag=True)
@click.argument('data', nargs=-1, type=click.Path(), required=True)
def load(data, path, db, verbose):
    '''Load data into database'''

    repo=Repository(path)

    for d in data_files(repo, data):
        if verbose:
            show_verbose(d, 'load')

@cli.command()
@click.option('--path', '-p', type=click.Path(), default=None, envvar='RENGUPATH')
@click.option('--db', '-d', envvar='RENGUDB')
@click.option('--verbose', '-v', envvar='RENGUVERBOSE', is_flag=True)
@click.argument('data', nargs=-1, type=click.Path(), required=True)
def test(data, path, db, verbose):
    '''Test data into database'''

    repo=Repository(path)

    for d in data_files(repo, data):
        if verbose:
            show_verbose(d, 'test')




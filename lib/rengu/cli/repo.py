# -*- coding: utf-8 -*-

# Rengu CLI repository commands

import click

from ..cli import cli

import rengu.repo

@cli.group()
def repo():
    pass

@repo.command()
@click.option('--repo', '-r', default=None, help='Rengu path')
def info(repo):
    r = rengu.repo.Repository(repo)

    click.echo("Rengu path = " + str(r))

@repo.command()
@click.option('--repo', '-r', default=None, help='Rengu path')
@click.option('--verbose', '-v', default=0, count=True, help='Verbosity level')
def check(repo, verbose):
    r = rengu.repo.Repository(repo)

    for i in r.check(verbosity=verbose):
        click.echo(i)


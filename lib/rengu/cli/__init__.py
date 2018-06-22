# -*- coding: utf-8 -*-

# Parent module for all CLI interactions

__all__= [
    "cli",
    "check",
    "repo",
    "tools"
]

import click

@click.group()
def cli():
    pass


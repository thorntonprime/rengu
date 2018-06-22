# -*- coding: utf-8 -*-

# Rengu CLI tools commands

import click
from ..cli import cli

@cli.command()
def prepare():
    import sh
    import sys

    modules = [
        "colorama",
        "tqdm",
        "sh",
        "click",
        "dask",
        "distributed",
        "yamllint"
    ]

    python = sh.Command(sys.executable)
    pip = python.bake("-m", "pip")
    for r in pip("install", "--user", *modules):
        print(r.strip())

# cli.add_command(prepare)


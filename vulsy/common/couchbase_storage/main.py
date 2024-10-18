"""Couchbase storage CLI."""

import time

import typer

from vulsy.common.couchbase_storage.setup.configuration import configure
from vulsy.common.couchbase_storage.setup.initialization import initialize_couchbase_server

couchbase_app = typer.Typer()


@couchbase_app.command()
def initialize() -> None:
    """Initialize Couchbase server from scratch."""
    typer.echo("Initialize new Couchbase server...")
    initialize_couchbase_server()
    typer.echo("Couchbase initialized.")


@couchbase_app.command()
def setup() -> None:
    """Set up Couchbase with the necessary buckets and collections."""
    typer.echo("Setting up Couchbase...")
    configure()
    typer.echo("Couchbase setup complete.")


@couchbase_app.command()
def full() -> None:
    """Initialize and set up Couchbase."""
    initialize()
    timeout = 10
    for i in range(timeout):
        typer.echo(f"Wait {timeout - i} ...")
        time.sleep(1)
    setup()

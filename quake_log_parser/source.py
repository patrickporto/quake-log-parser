from quake_log_parser.cli import cli
import click
from rich import print

from quake_log_parser.repositories.source_repository import SourceRepository


@cli.group()
def source():
    pass


@source.command()
@click.argument("uri")
def add(uri: str):
    print(f"Adding URL [bold magenta]{uri}[/bold magenta]")
    source_repository = SourceRepository()
    source_repository.add_source(uri)
    print(f"URL [bold magenta]{uri}[/bold magenta] added successfully")

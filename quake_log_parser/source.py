from quake_log_parser.cli import cli
import click
from rich import print

from quake_log_parser.repositories.source_repository import SourceRepository


@cli.group()
def source():
    pass


@source.command()
@click.argument("url")
def add_url(url: str):
    print(f"Adding URL [bold magenta]{url}[/bold magenta]")
    source_repository = SourceRepository()
    source_repository.add_source(url)
    print(f"URL [bold magenta]{url}[/bold magenta] added successfully")

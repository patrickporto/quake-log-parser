import duckdb

from quake_log_parser.cli import cli
import click
from rich import print
from quake_log_parser import settings
import hashlib


@cli.group()
def source():
    pass


@source.command()
@click.argument("url")
def add_url(url: str):
    with duckdb.connect(settings.DATABASE_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS source (hash VARCHAR(64) PRIMARY KEY , uri VARCHAR(256))")
        print(f"Adding URL [bold magenta]{url}[/bold magenta]")
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        conn.execute(f"INSERT INTO source VALUES ('{url_hash}', '{url}')")

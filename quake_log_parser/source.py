from quake_log_parser.cli import cli
import toml
import click
from rich import print
from quake_log_parser.models.source_url import SourceUrl
from quake_log_parser import settings


@cli.group()
def source():
    pass


@source.command()
@click.argument("url")
def add_url(url: str):
    print(f"Adding URL [bold magenta]{url}[/bold magenta]")
    with open(settings.CONFIG_NAME, "w+") as logparser_raw:
        logparser_config = toml.load(logparser_raw)
        if "source" not in logparser_config:
            logparser_config["source"] = {}
        if "urls" not in logparser_config["source"]:
            logparser_config["source"]["urls"] = []
        logparser_config["source"]["urls"].append(SourceUrl(url=url).model_dump())
        toml.dump(logparser_config, logparser_raw)

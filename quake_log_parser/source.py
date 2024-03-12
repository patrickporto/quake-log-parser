from cli import cli
import toml
import click
from rich import print


CONFIG_NAME = "logparser.toml"


@cli.group()
def source():
    pass


@source.command()
@click.argument("url")
def add_url(url: str):
    print(f"Adding URL [bold magenta]{url}[/bold magenta]")
    with open(CONFIG_NAME, "w+") as logparser_raw:
        config = toml.load(logparser_raw)
        if "source" not in config:
            config["source"] = {}
        if "urls" not in config["source"]:
            config["source"]["urls"] = []
        config["source"]["urls"].append(url)
        toml.dump(config, logparser_raw)

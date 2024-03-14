import json

import click

from quake_log_parser.cli import cli
from quake_log_parser.ranking.matches import matches_ranking

from quake_log_parser.repositories.log_record_repository import LogRecordRepository


@cli.group()
def report():
    pass


@report.command()
def player_ranking():
    log_record_repository = LogRecordRepository()
    matches = matches_ranking(
        [log_record for (log_record,) in log_record_repository.get_log_records()]
    )
    click.echo(json.dumps(matches))

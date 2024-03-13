from cli import cli
import duckdb
from quake_log_parser import settings
from rich import print
from dataclasses import dataclass
from quake_log_parser.transforms.tokenization import Tokenizer


@cli.command()
def player_ranking():
    with duckdb.connect(settings.DATABASE_FILE) as conn:
        result = conn.execute("SELECT log FROM log_record ORDER BY row_number")
        for (log_record,) in result.fetchall():
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(log_record)
            print(tokens)

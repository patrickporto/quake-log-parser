from cli import cli
import duckdb
from quake_log_parser import settings


@cli.command()
def player_ranking():
    with duckdb.connect(settings.DATABASE_FILE) as conn:
        result = conn.execute("SELECT log FROM log_record ORDER BY row_number")
        for row in result.fetchall():
            print(row[0])

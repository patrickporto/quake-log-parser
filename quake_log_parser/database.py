import duckdb

from quake_log_parser import settings
from quake_log_parser.cli import cli
from rich import print


@cli.group()
def database():
    pass


CREATE_LOG_RECORD_TABLE = """
CREATE TABLE IF NOT EXISTS log_record (
    idempotency_key VARCHAR(256) PRIMARY KEY NOT NULL,
    source_checksum VARCHAR(64),
    row_number INTEGER,
    log TEXT
)
"""

CREATE_SOURCE_TABLE = """
CREATE TABLE IF NOT EXISTS source (
    hash VARCHAR(64) PRIMARY KEY,
    uri VARCHAR(256)
)
"""


@database.command()
def init():
    print("Initializing database")
    with duckdb.connect(settings.DATABASE_FILE) as conn:
        print("Creating log_record table")
        conn.execute(CREATE_LOG_RECORD_TABLE)
        print("Creating source table")
        conn.execute(CREATE_SOURCE_TABLE)

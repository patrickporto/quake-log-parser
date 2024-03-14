import hashlib

import duckdb

from quake_log_parser import settings


CREATE_SOURCE_TABLE = "CREATE TABLE IF NOT EXISTS source (hash VARCHAR(64) PRIMARY KEY , uri VARCHAR(256))"


class SourceRepository:
    def add_source(self, url: str):
        with duckdb.connect(settings.DATABASE_FILE) as conn:
            conn.execute(CREATE_SOURCE_TABLE)
            url_hash = hashlib.sha256(url.encode()).hexdigest()
            conn.execute(f"INSERT INTO source VALUES ('{url_hash}', '{url}')")

    def get_sources(self):
        with duckdb.connect(settings.DATABASE_FILE) as conn:
            conn.execute(CREATE_SOURCE_TABLE)
            return conn.execute("SELECT uri FROM source").fetchall()

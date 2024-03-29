import hashlib

import duckdb

from quake_log_parser import settings


class SourceRepository:
    def add_source(self, uri: str):
        with duckdb.connect(settings.DATABASE_FILE) as conn:
            url_hash = hashlib.sha256(uri.encode()).hexdigest()
            try:
                conn.execute(f"INSERT INTO source VALUES ('{url_hash}', '{uri}')")
            except duckdb.ConstraintException:
                pass

    def get_sources(self):
        with duckdb.connect(settings.DATABASE_FILE) as conn:
            return conn.execute("SELECT uri FROM source").fetchall()

import hashlib

import duckdb

from quake_log_parser import settings


class LogRecordRepository:
    def add_log_record(
        self, source_checksum: str, row_number: int, log_record: str
    ) -> None:
        with duckdb.connect(settings.DATABASE_FILE) as conn:
            idempotency_key = hashlib.sha256(
                (source_checksum + str(row_number)).encode()
            ).hexdigest()
            try:
                conn.execute(
                    f"INSERT INTO log_record VALUES "
                    f"('{idempotency_key}', '{source_checksum}', {row_number}, '{log_record}')"
                )
            except duckdb.ConstraintException:
                pass

    def get_log_records(self):
        with duckdb.connect(settings.DATABASE_FILE) as conn:
            return conn.execute("SELECT * FROM log_record").fetchall()

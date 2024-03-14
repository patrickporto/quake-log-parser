from quake_log_parser.cli import cli
import duckdb
from quake_log_parser import settings
from rich import print
import requests
import zlib

from quake_log_parser.repositories.source_repository import SourceRepository


@cli.group()
def ingestion():
    pass


STREAM_CHUNK_SIZE = 8192


@ingestion.command()
def pull():
    settings.INGESTION_PATH.mkdir(parents=True, exist_ok=True)

    source_repository = SourceRepository()
    sources = source_repository.get_sources()
    for (uri,) in sources:
        print(f"Downloading URL [bold magenta]{uri}[/bold magenta]")
        filename = uri.split("/")[-1]
        with requests.get(uri, stream=True) as response:
            response.raise_for_status()
            with open(settings.INGESTION_PATH / filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=STREAM_CHUNK_SIZE):
                    file.write(chunk)


@ingestion.command()
def run():
    with duckdb.connect(settings.DATABASE_FILE) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS log_record (idempotency_key VARCHAR(64), row_number INTEGER, log TEXT)"
        )

        for file in settings.INGESTION_PATH.iterdir():
            print(f"Ingesting file [bold magenta]{file.name}[/bold magenta]")
            with open(file, "r") as log_file:
                idempotency_key = None
                while buffer := log_file.read(STREAM_CHUNK_SIZE):
                    if idempotency_key is None:
                        idempotency_key = zlib.adler32(buffer.encode())
                    else:
                        idempotency_key = zlib.adler32(buffer.encode(), idempotency_key)
                print(
                    f"Idempotency key: [bold magenta]{idempotency_key}[/bold magenta]"
                )
                log_file.seek(0)
                for row_number, line in enumerate(log_file):
                    conn.execute(
                        f"INSERT INTO log_record VALUES ('{hash}', {row_number}, '{line}')"
                    )

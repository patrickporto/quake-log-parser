from cli import cli
import duckdb
from quake_log_parser import settings
from rich import print
import toml
import requests
import zlib


@cli.group()
def ingestion():
    pass


STREAM_CHUNK_SIZE = 8192


@ingestion.command()
def pull():
    settings.INGESTION_PATH.mkdir(parents=True, exist_ok=True)
    with open(settings.CONFIG_NAME, "r") as logparser_raw:
        logparser_config = toml.load(logparser_raw)
        if "source" not in logparser_config:
            print("No source defined")
            return
        if "urls" not in logparser_config["source"]:
            print("No URLs defined")
            return
        for url in logparser_config["source"]["urls"]:
            print(f"Downloading URL [bold magenta]{url['url']}[/bold magenta]")
            filename = url['url'].split("/")[-1]
            with requests.get(url['url'], stream=True) as response:
                response.raise_for_status()
                with open(settings.INGESTION_PATH / filename, "wb") as file:
                    for chunk in response.iter_content(chunk_size=STREAM_CHUNK_SIZE):
                        file.write(chunk)


@ingestion.command()
def run():
    with duckdb.connect(settings.DATABASE_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS log_record (idempotency_key VARCHAR(64), row_number INTEGER, log TEXT)")

        for file in settings.INGESTION_PATH.iterdir():
            print(f"Ingesting file [bold magenta]{file.name}[/bold magenta]")
            with open(file, "r") as log_file:
                idempotency_key = None
                while buffer := log_file.read(STREAM_CHUNK_SIZE):
                    if idempotency_key is None:
                        idempotency_key = zlib.adler32(buffer.encode())
                    else:
                        idempotency_key = zlib.adler32(buffer.encode(), idempotency_key)
                print(f"Idempotency key: [bold magenta]{idempotency_key}[/bold magenta]")
                log_file.seek(0)
                for row_number, line in enumerate(log_file):
                    conn.execute(f"INSERT INTO log_record VALUES ('{hash}', {row_number}, '{line}')")

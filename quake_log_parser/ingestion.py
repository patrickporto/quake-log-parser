from quake_log_parser.cli import cli
from quake_log_parser import settings
from rich import print
import requests
import zlib

from quake_log_parser.repositories.log_record_repository import LogRecordRepository
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
        print(f"URL [bold magenta]{uri}[/bold magenta] downloaded successfully")


@ingestion.command()
def run():
    log_record_repository = LogRecordRepository()
    for file in settings.INGESTION_PATH.iterdir():
        with open(file, "r") as log_file:
            file_checksum = None
            while buffer := log_file.read(STREAM_CHUNK_SIZE):
                if file_checksum is None:
                    file_checksum = zlib.adler32(buffer.encode())
                else:
                    file_checksum = zlib.adler32(buffer.encode(), file_checksum)
            print(
                f"Ingesting file [bold magenta]{file.name}[/bold magenta] (checksum: {file_checksum})"
            )
            log_file.seek(0)
            for row_number, line in enumerate(log_file):
                log_record_repository.add_log_record(
                    source_checksum=str(file_checksum),
                    row_number=row_number,
                    log_record=line,
                )
    print("Ingestion complete")

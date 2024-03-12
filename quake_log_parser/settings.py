import tempfile
from pathlib import Path


DATABASE_FILE = 'quake_log.db'
CONFIG_NAME = "logparser.toml"

INGESTION_PATH = Path.home() / ".quake_log_parser" / "ingestion"

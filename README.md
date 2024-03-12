# Quake Log Parser

This is a simple log parser for Quake 3 Arena games. It was developed as a test for a job interview.


## Usage

To use the parser, simply run the following command:

```bash
poetry run python quake_log_parser source add-url <URL>
```

Where `<URL>` is the URL of the log file to be parsed.

Example:

```bash
poetry run python quake_log_parser source add-url https://gist.githubusercontent.com/cloudwalk-tests/be1b636e58abff14088c8b5309f575d8/raw/df6ef4a9c0b326ce3760233ef24ae8bf
a8e33940/qgames.log
```

# Quake Log Parser

This is a simple log parser for Quake 3 Arena games. It reads a log file and outputs a JSON file with the players ranking.


## Prerequisites

- Docker
- Make

## Getting Started

Clone the repository and run the following command to build the docker image and execute the parser:

```
make run
```

The `player-ranking-output.json` will be created in the root directory.

## Running the tests

To run the tests, execute the following command:

```
make test
```

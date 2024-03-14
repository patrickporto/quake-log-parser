import json

from quake_log_parser.cli import cli
from rich import print

from quake_log_parser.repositories.log_record_repository import LogRecordRepository
from quake_log_parser.transforms.tokenization import Tokenizer, Token, Entity


WORLD_ID = "1022"


class Game:
    def __init__(self):
        self.players = {}
        self.kills = {}

    def add_player(self, player_id):
        self.players[player_id] = player_id
        self.kills[player_id] = 0

    def change_player_name(self, player_id, player_name):
        self.players[player_id] = player_name

    def add_kill(self, killer, victim):
        if killer == WORLD_ID:
            self.kills[victim] = (
                self.kills.get(victim, 0) - 1 if self.kills.get(victim, 0) > 0 else 0
            )
        else:
            self.kills[killer] = self.kills.get(killer, 0) + 1

    def to_dict(self):
        players = list(set(self.players.values()))
        kills = {
            self.players[player_id]: player_score
            for player_id, player_score in self.kills.items()
        }
        return {"players": players, "kills": kills}


@cli.command()
def player_ranking():
    games = {}
    current_game = None

    log_record_repository = LogRecordRepository()

    for (log_record,) in log_record_repository.get_log_records():
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(log_record)
        match tokens:
            case [_, Token(value="InitGame", entity=Entity.COMMAND), *rest]:
                game_index = len(games.keys()) + 1
                current_game = f"game_{game_index}"
                games[current_game] = Game()
            case [_, Token(value="ClientConnect", entity=Entity.COMMAND), *rest]:
                arguments = [
                    token for token in rest if token.entity == Entity.COMMAND_ARGUMENT
                ]
                player_id = arguments[0].value
                games[current_game].add_player(player_id)
            case [
                _,
                Token(value="ClientUserinfoChanged", entity=Entity.COMMAND),
                *rest,
            ]:
                arguments = [
                    token for token in rest if token.entity == Entity.COMMAND_ARGUMENT
                ]
                player_id = arguments[0].value
                player_name = arguments[1].value.split("\\")[1]
                games[current_game].change_player_name(player_id, player_name)
            case [_, Token(value="Kill", entity=Entity.COMMAND), *rest]:
                arguments = [
                    token for token in rest if token.entity == Entity.COMMAND_ARGUMENT
                ]
                killer = arguments[0].value
                victim = arguments[1].value
                games[current_game].add_kill(killer, victim)
            case _:
                ...

    for game_key, game in games.items():
        games[game_key] = game.to_dict()

    print(json.dumps(games))

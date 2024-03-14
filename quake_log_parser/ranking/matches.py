from quake_log_parser.parser.token import Token
from quake_log_parser.parser.token_entity import Entity
from quake_log_parser.parser.tokenization import Tokenizer
from quake_log_parser.ranking.game import Game


def matches_ranking(log_records: list[str]):
    games = {}
    current_game = None

    for log_record in log_records:
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
                cause = arguments[-1].value

                games[current_game].add_kill(killer, victim, cause)
            case _:
                ...

    for game_key, game in games.items():
        games[game_key] = game.get_ranking()
    return games

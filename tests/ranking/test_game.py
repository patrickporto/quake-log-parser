from quake_log_parser.quake.constants import WORLD_ID
from quake_log_parser.quake.death_cause import DeathCause
from quake_log_parser.ranking.game import Game


def test_player_kill_player():
    game = Game()
    game.add_player(2)
    game.add_player(3)
    game.add_kill(2, 3, cause=DeathCause.MOD_RAILGUN)
    assert game.kills[2] == 1
    assert game.kills[3] == 0


def test_world_kill_player_without_score():
    game = Game()
    game.add_player(2)
    game.add_player(3)
    game.add_kill(WORLD_ID, 2, cause=DeathCause.MOD_FALLING)
    assert game.kills[2] == 0
    assert game.kills[3] == 0


def test_world_kill_player_with_score():
    game = Game()
    game.add_player(2)
    game.add_player(3)
    game.add_kill(2, 3, cause=DeathCause.MOD_RAILGUN)
    game.add_kill(WORLD_ID, 2, cause=DeathCause.MOD_FALLING)
    assert game.kills[2] == 0
    assert game.kills[3] == 0

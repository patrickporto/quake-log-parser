from collections import defaultdict

from quake_log_parser.quake.constants import WORLD_ID


class Game:
    def __init__(self):
        self.players = {}
        self.kills = defaultdict(int)
        self.total_kills = 0
        self.death_causes = defaultdict(int)

    def add_player(self, player_id):
        self.players[player_id] = player_id
        self.kills[player_id] = 0

    def change_player_name(self, player_id, player_name):
        self.players[player_id] = player_name

    def add_kill(self, killer, victim, cause):
        self.total_kills += 1
        self.death_causes[cause] = self.death_causes[cause] + 1
        if killer == WORLD_ID:
            self.kills[victim] = self.kills[victim] - 1 if self.kills[victim] > 0 else 0
        elif killer != victim:
            self.kills[killer] = self.kills[killer] + 1

    def get_ranking(self):
        players = []
        kills = {}
        for player_id, player_name in self.players.items():
            players.append(player_name)
            kills[player_name] = self.kills[player_id]
        return {
            "total_kills": self.total_kills,
            "players": players,
            "kills": kills,
            "kills_by_means": self.death_causes,
        }

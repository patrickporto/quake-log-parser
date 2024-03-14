from quake_log_parser.quake.constants import WORLD_ID


class Game:
    def __init__(self):
        self.players = {}
        self.kills = {}
        self.total_kills = 0

    def add_player(self, player_id):
        self.players[player_id] = player_id
        self.kills[player_id] = 0

    def change_player_name(self, player_id, player_name):
        self.players[player_id] = player_name

    def add_kill(self, killer, victim):
        self.total_kills += 1
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
        return {"total_kills": self.total_kills, "players": players, "kills": kills}

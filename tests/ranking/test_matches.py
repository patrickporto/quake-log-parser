from quake_log_parser.ranking.matches import matches_ranking


def test_simple_match(simple_match_fixture):
    matches = matches_ranking(simple_match_fixture)
    assert matches == {
        "game_1": {
            "total_kills": 4,
            "players": ["Dono da Bola", "Isgalamido", "Zeh"],
            "kills": {
                "Isgalamido": 1,
                "Dono da Bola": 0,
                "Zeh": 0,
            },
        }
    }

import pytest


@pytest.fixture()
def simple_match_fixture():
    with open("tests/fixtures/simple-match.txt", "r") as fixture:
        return fixture.readlines()

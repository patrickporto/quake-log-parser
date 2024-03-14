from quake_log_parser.parser.tokenization import Tokenizer
from quake_log_parser.parser.token import Token
from quake_log_parser.parser.token_entity import Entity


def test_empty_log_record():
    log_record = ""
    expected_tokens = []
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_simple_text():
    log_record = "Hello"
    expected_tokens = [Token(value="Hello", entity=Entity.WORD)]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_simple_number():
    log_record = "1234"
    expected_tokens = [Token(value="1234", entity=Entity.NUMBER)]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_time():
    log_record = "20:40"
    expected_tokens = [Token(value="20:40", entity=Entity.TIME)]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_time_and_command():
    log_record = "  0:00 InitGame:"
    expected_tokens = [
        Token(value="0:00", entity=Entity.TIME),
        Token(value="InitGame", entity=Entity.COMMAND),
        Token(value=":", entity=Entity.DELIMITER),
    ]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_command_and_arguments():
    log_record = "20:40 Item: 2 weapon_rocketlauncher"
    expected_tokens = [
        Token(value="20:40", entity=Entity.TIME),
        Token(value="Item", entity=Entity.COMMAND),
        Token(value=":", entity=Entity.DELIMITER),
        Token(value="2", entity=Entity.COMMAND_ARGUMENT),
        Token(value="weapon_rocketlauncher", entity=Entity.COMMAND_ARGUMENT),
    ]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_kill_command():
    log_record = "21:42 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT"
    expected_tokens = [
        Token(value="21:42", entity=Entity.TIME),
        Token(value="Kill", entity=Entity.COMMAND),
        Token(value=":", entity=Entity.DELIMITER),
        Token(value="1022", entity=Entity.COMMAND_ARGUMENT),
        Token(value="2", entity=Entity.COMMAND_ARGUMENT),
        Token(value="22", entity=Entity.COMMAND_ARGUMENT),
        Token(value=":", entity=Entity.DELIMITER),
        Token(value="<world>", entity=Entity.COMMAND_ARGUMENT),
        Token(value="killed", entity=Entity.KEYWORD),
        Token(value="Isgalamido", entity=Entity.COMMAND_ARGUMENT),
        Token(value="by", entity=Entity.KEYWORD),
        Token(value="MOD_TRIGGER_HURT", entity=Entity.COMMAND_ARGUMENT),
    ]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_client_user_info_changed():
    log_record = r"20:34 ClientUserinfoChanged: 2 n\Dono da Bola\t\0\model\sarge/krusade\hmodel\sarge/krusade\g_redteam\\g_blueteam\\c1\5\c2\5\hc\95\w\0\l\0\tt\0\tl\0"
    expected_tokens = [
        Token(value="20:34", entity=Entity.TIME),
        Token(value="ClientUserinfoChanged", entity=Entity.COMMAND),
        Token(value=":", entity=Entity.DELIMITER),
        Token(value="2", entity=Entity.COMMAND_ARGUMENT),
        Token(
            value=r"n\Dono da Bola\t\0\model\sarge/krusade\hmodel\sarge/krusade\g_redteam\\g_blueteam\\c1\5\c2\5\hc\95\w\0\l\0\tt\0\tl\0",
            entity=Entity.COMMAND_ARGUMENT,
        ),
    ]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens

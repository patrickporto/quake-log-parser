from quake_log_parser.transforms.tokenization import Tokenizer, Token, Entity



def test_empty_log_record():
    log_record = ''
    expected_tokens = []
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_simple_text():
    log_record = 'Hello'
    expected_tokens = [Token(value='Hello')]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_simple_number():
    log_record = '1234'
    expected_tokens = [Token(value='1234')]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_time():
    log_record = '20:40'
    expected_tokens = [Token(value='20:40', entity=Entity.TIME)]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_time_and_command():
    log_record = '  0:00 InitGame:'
    expected_tokens = [Token(value='0:00', entity=Entity.TIME), Token(value='InitGame', entity=Entity.COMMAND)]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens


def test_command_and_arguments():
    log_record = '20:40 Item: 2 weapon_rocketlauncher'
    expected_tokens = [
        Token(value='20:40', entity=Entity.TIME),
        Token(value='Item', entity=Entity.COMMAND),
        Token(value='2', entity=Entity.COMMAND_ARGUMENT),
        Token(value='weapon_rocketlauncher', entity=Entity.COMMAND_ARGUMENT),
    ]
    tokenizer = Tokenizer()
    assert tokenizer.tokenize(log_record) == expected_tokens

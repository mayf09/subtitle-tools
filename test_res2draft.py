import pytest

from utils.get_valid_string import get_valid_string

@pytest.mark.parametrize('text, res',
[
    (' ab123\'', 'ab123'),
    ('I\'m going to', 'Imgoingto'),
    ('12,345', '12345')
]
)
def test_get_valid_string(text, res):
    assert get_valid_string(text) == res

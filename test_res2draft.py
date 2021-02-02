import pytest

from utils.res2draft import get_only_letters

@pytest.mark.parametrize('text, res',
[
    (' ab123\'', 'ab123'),
    ('I\'m going to', 'I\'m going to'),
    ('12,345', '12,345')
]
)
def test_get_only_letters(text, res):
    assert get_only_letters(text) == res

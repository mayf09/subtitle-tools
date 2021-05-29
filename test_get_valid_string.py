import pytest

from utils.get_valid_string import get_valid_string


@pytest.mark.parametrize('s, res', [
    ('1s,', '1s'),
    ('2%', '2%')
])
def test_get_valid_string(s, res):
    assert get_valid_string(s) == res

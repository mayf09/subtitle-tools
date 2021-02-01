import pytest

from utils.list_diff import get_list_diff


@pytest.mark.parametrize('l1, l2, res', [
    (
        ['a', 'bc', 'def', 'g'],
        ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        [(1, 2, 1, 3), (2, 3, 3, 6)]
    ),
    (
        ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        ['a', 'bc', 'def', 'g'],
        [(1, 3, 1, 2), (3, 6, 2, 3)],
    ),
    (
        ['a', 'b', 'c', 'def', 'g'],
        ['a', 'bc', 'd', 'e', 'f', 'g'],
        [(1, 3, 1, 2), (3, 4, 2, 5)]
    ),
    (
        ['a', 'bc', 'de', 'f'],
        ['a', 'b', 'cd', 'e', 'f'],
        [(1, 3, 1, 4)]
    )
])
def test_list_diff(l1, l2, res):
    assert get_list_diff(l1, l2) == res

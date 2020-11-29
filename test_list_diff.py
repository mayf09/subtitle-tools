import pytest

from utils.list_diff import ListDiffType
from utils.list_diff import get_list_diff


@pytest.mark.parametrize('l1, l2, res', [
    (
        ['a', 'bc', 'def', 'g'],
        ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        [(ListDiffType.EXPAND, 1, 2), (ListDiffType.EXPAND, 2, 3)]
    ),
    (
        ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        ['a', 'bc', 'def', 'g'],
        [(ListDiffType.MERGE, 1, 2), (ListDiffType.MERGE, 3, 3)],
    ),
    (
        ['a', 'b', 'c', 'def', 'g'],
        ['a', 'bc', 'd', 'e', 'f', 'g'],
        [(ListDiffType.MERGE, 1, 2), (ListDiffType.EXPAND, 3, 3)]
    )
])
def test_list_diff(l1, l2, res):
    assert get_list_diff(l1, l2) == res

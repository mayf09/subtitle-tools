from datetime import timedelta

import pytest

from draft_srt import (
    DraftSrt,
    TimeOffset,
    TimeOffsetParseException
)


@pytest.fixture
def draft_srt():
    content = '000,100 100,200 200,300 300,400 400,500\none two three| four five\n一二三|四五'
    return DraftSrt(
        index=1,
        start=timedelta(0, 10, 000),
        end=timedelta(0, 20, 200),
        content=content
    )


@pytest.fixture
def draft_srts():
    return [
        DraftSrt(
            index=1,
            start=timedelta(0, 10, 100),
            end=timedelta(0, 20, 200),
            content='000,100 100,200 200,300 300,400 400,500\none two three| four five\n一二三|四五六七八'
        ),
        DraftSrt(
            index=2,
            start=timedelta(0, 30, 300),
            end=timedelta(0, 40, 400),
            content='000,100 100,200\nsix seven'
        ),
        DraftSrt(
            index=3,
            start=timedelta(0, 50, 500),
            end=timedelta(0, 60, 600),
            content='000,100 100,200 200,300\neight| nine| ten\n|九|十'
        )
    ]


class TestDraftSrt:

    def test_valid_draft_srt(self, draft_srt):
        assert draft_srt.has_en_text() == True
        assert draft_srt.has_zh_text() == True
        assert draft_srt.check_time_offset() == True
        assert draft_srt.check_zh_text() == True
        assert len(draft_srt.time_offset) == 5
        assert draft_srt.en_text == 'one two three| four five'
        assert draft_srt.zh_text == '一二三|四五'
        expect_res = [
            'one two three\n一二三',
            'four five\n四五'
        ]
        for i, srt in enumerate(draft_srt.get_part_srts()):
            if srt is not None:
                # print(srt.to_srt())
                assert srt.content == expect_res[i]
        assert len(draft_srt.get_part_srts()) == 2

        draft_srt.en_text = 'one two three four five six seven'
        assert draft_srt.en_text == 'one two three four five six seven'

    def test_to_time_offset(self):
        time_offset_string = '010,100'
        time_offset_string_invalid = '010,100,110'

        assert DraftSrt.to_time_offset(time_offset_string) == TimeOffset(10, 100)
        with pytest.raises(TimeOffsetParseException):
            DraftSrt.to_time_offset(time_offset_string_invalid)

    def test_to_final_srts(self, draft_srts):
        final_srts = DraftSrt.to_final_srts(draft_srts)
        expect_res = [
            'one two three\n一二三',
            'four five six seven eight\n四五六七八',
            'nine\n九',
            'ten\n十'
        ]
        for i, srt in enumerate(final_srts):
            # print(srt.to_srt())
            assert srt.content == expect_res[i]


    @pytest.mark.parametrize('text, res',
    [
        ('{} one two three {four,five,six} {seven - -}', 'one two three four five six seven'),
        ('{1.2 -}', '1.2'),
        ('{[] -}', '[]'),
        ('{\\{one\\} -}', '\\{one\\}')
    ],
    scope='class',
    )
    def test_fix_en_text(self, text, res):
        assert DraftSrt.fix_en_text(text) == res

    def test_skip_split_text(self):
        content = '000,100 100,200 200,300 300,400 400,500\none two\\| three four five\n一二\\|三四五'
        draft_srt = DraftSrt(
            index=1,
            start=timedelta(0, 10, 100),
            end=timedelta(0, 20, 200),
            content=content
        )
        assert len(draft_srt.get_part_srts()) == 1

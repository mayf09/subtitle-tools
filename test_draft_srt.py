from datetime import timedelta

import pytest

from draft_srt import (
    DraftSrt,
    TimeOffset,
    TimeOffsetParseException
)


@pytest.fixture
def draft_srt():
    content = '000,100 200,300 300,500\nabc| def| g|\n一二|三四|五|'
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
            content='000,100 100,200\nabc| de\n一二三|四五'
        ),
        DraftSrt(
            index=2,
            start=timedelta(0, 30, 300),
            end=timedelta(0, 40, 400),
            content='200,300\nfg\n六七'
        ),
        DraftSrt(
            index=3,
            start=timedelta(0, 50, 500),
            end=timedelta(0, 60, 600),
            content='300,400 400,500 500,600\nhi| jkl| mn\n|八|九'
        )
    ]


class TestDraftSrt:

    def test_valid_draft_srt(self, draft_srt):
        assert draft_srt.has_en_text() == True
        assert draft_srt.has_zh_text() == True
        assert draft_srt.check_time_offset() == True
        assert draft_srt.check_zh_text() == True
        assert len(draft_srt.time_offset) == 3
        assert draft_srt.en_text == 'abc| def| g|'
        assert draft_srt.zh_text == '一二|三四|五|'
        expect_res = [
            'abc\n一二',
            'def\n三四',
            'g\n五'
        ]
        for i, srt in enumerate(draft_srt.get_part_srts()):
            if srt is not None:
                # print(srt.to_srt())
                assert srt.content == expect_res[i]
        assert len(draft_srt.get_part_srts()) == 4

        draft_srt.en_text = 'abcdefg'
        assert draft_srt.en_text == 'abcdefg'

    def test_to_time_offset(self):
        time_offset_string = '010,100'
        time_offset_string_invalid = '010,100,110'

        assert DraftSrt.to_time_offset(time_offset_string) == TimeOffset(10, 100)
        with pytest.raises(TimeOffsetParseException):
            DraftSrt.to_time_offset(time_offset_string_invalid)

    def test_to_final_srts(self, draft_srts):
        final_srts = DraftSrt.to_final_srts(draft_srts)
        expect_res = [
            'abc\n一二三',
            'de fg hi\n四五六七',
            'jkl\n八',
            'mn\n九'
        ]
        for i, srt in enumerate(final_srts):
            # print(srt.to_srt())
            assert srt.content == expect_res[i]


    @pytest.mark.parametrize('text, res',
    [
        ('{} a bc {d,ef} {g - -}', 'a bc d ef g'),
        ('{1.2 -}', '1.2'),
        ('{[] -}', '[]'),
    ],
    scope='class',
    )
    def test_fix_en_text(self, text, res):
        assert DraftSrt.fix_en_text(text) == res

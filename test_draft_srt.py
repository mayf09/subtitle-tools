from draft_srt import DraftSrt

import datetime


class TestDraftSrt:

    content = '000:090 100:200\nabc de\n一二三'

    def test_valid_draft_srt(self):

        draft_srt = DraftSrt(
            index=1,
            start=datetime.timedelta(0, 10, 100),
            end=datetime.timedelta(0, 20, 200),
            content=self.content
        )

        assert draft_srt.has_en_text() == True
        assert draft_srt.has_zh_text() == True
        assert draft_srt.check_time_offset() == True
        assert draft_srt.check_zh_text() == True
        assert len(draft_srt.time_offset) == 2
        assert draft_srt.en_text == 'abc de'
        assert draft_srt.zh_text == '一二三'

        draft_srt.en_text = 'abc defg'
        assert draft_srt.en_text == 'abc defg'

from draft_srt import DraftSrt

import datetime


class TestDraftSrt:

    content = '000,100 200,300 300,500\nabc| def| g|\n一二|三四|五|'

    def test_valid_draft_srt(self):

        draft_srt = DraftSrt(
            index=1,
            start=datetime.timedelta(0, 10, 000),
            end=datetime.timedelta(0, 20, 200),
            content=self.content
        )

        assert draft_srt.has_en_text() == True
        assert draft_srt.has_zh_text() == True
        assert draft_srt.check_time_offset() == True
        assert draft_srt.check_zh_text() == True
        assert len(draft_srt.time_offset) == 3
        assert draft_srt.en_text == 'abc| def| g|'
        assert draft_srt.zh_text == '一二|三四|五|'
        for _ in draft_srt.get_part_srts():
            if _ is not None:
                print(_.to_srt())
        assert len(draft_srt.get_part_srts()) == 4

        draft_srt.en_text = 'abcdefg'
        assert draft_srt.en_text == 'abcdefg'

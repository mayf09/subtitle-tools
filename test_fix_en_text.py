from draft_srt import DraftSrt


class TestFixEnText:

    text = '{} a bc {d,ef} {g - -}'

    def test_fix_en_text(self):
        assert DraftSrt.fix_en_text(self.text) == 'a bc d ef g'

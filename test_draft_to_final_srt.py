from datetime import timedelta


from draft_srt import DraftSrt


class TestDraftToFinalSrt:

    def test_to_final_srts(self):

        draft_srts = [
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

        final_srts = DraftSrt.to_final_srts(draft_srts)

        for srt in final_srts:
            print(srt.to_srt())

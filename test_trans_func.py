from datetime import timedelta

from draft_srt import DraftSrt
from utils.trans_func import trans


def test_trans():

    subs = [
        DraftSrt(
            index=1,
            start=timedelta(0, 10, 100),
            end=timedelta(0, 20, 200),
            content='\n'.join(['000,100 100,200 200,300 300,400 400,500', 'one two three| four five'])
        ),
        DraftSrt(
            index=2,
            start=timedelta(0, 30, 100),
            end=timedelta(0, 40, 200),
            content='\n'.join(['000,100 100,200 200,300', 'six| seven| eight|'])
        ),
        DraftSrt(
            index=3,
            start=timedelta(0, 50, 100),
            end=timedelta(1, 00, 200),
            content='\n'.join(['000,100 100,200 200,300', 'nine| ten| eleven'])
        ),
        DraftSrt(
            index=4,
            start=timedelta(1, 10, 100),
            end=timedelta(1, 20, 200),
            content='\n'.join(['000,100 100,200', 'twelve thirteen'])
        ),
        DraftSrt(
            index=5,
            start=timedelta(1, 30, 100),
            end=timedelta(1, 40, 200),
            content='\n'.join(['000,100 200,300', 'fourteen| fivteen'])
        ),
        DraftSrt(
            index=6,
            start=timedelta(1, 50, 100),
            end=timedelta(2, 00, 200),
            content='\n'.join(['000,100', 'sixteen'])
        )
    ]

    # for _ in subs:
    #     print(_.text)

    trans(subs, 10, lambda l: [str(len(_.split())) for _ in l])

    for _ in subs:
        print(_.to_srt())

    # real_sub_gen = get_next_real_sub(subs)
    # for _ in real_sub_gen:
    #     print(_)
from datetime import timedelta

from draft_srt import DraftSrt
from utils.trans_func import trans


def test_trans():

    subs = [
        DraftSrt(
            index=1,
            start=timedelta(0, 10, 100),
            end=timedelta(0, 10, 200),
            content='\n'.join(['000,100 200,300 400,500 600, 700', 'a bc| d e'])
        ),
        DraftSrt(
            index=2,
            start=timedelta(0, 20, 100),
            end=timedelta(0, 20, 200),
            content='\n'.join(['000,100 200,300 400,500', 'f| g| h|'])
        ),
        DraftSrt(
            index=3,
            start=timedelta(0, 30, 100),
            end=timedelta(0, 30, 200),
            content='\n'.join(['000,100 200,300 400,500', 'f| g| h|'])
        ),
        DraftSrt(
            index=4,
            start=timedelta(0, 40, 100),
            end=timedelta(0, 40, 200),
            content='\n'.join(['000,100 200,300 400,500', 'i j k'])
        ),
        DraftSrt(
            index=5,
            start=timedelta(0, 50, 100),
            end=timedelta(0, 50, 200),
            content='\n'.join(['000,100 200,300', 'l| m'])
        ),
        DraftSrt(
            index=6,
            start=timedelta(0, 60, 100),
            end=timedelta(0, 60, 200),
            content='\n'.join(['000,100', 'n'])
        )
    ]

    # for _ in subs:
    #     print(_.text)

    trans(subs, 10, lambda l: [str(len(_)) for _ in l])

    for _ in subs:
        print(_.to_srt())

    # real_sub_gen = get_next_real_sub(subs)
    # for _ in real_sub_gen:
    #     print(_)
from datetime import timedelta

import srt

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
            end=timedelta(0, 60, 200),
            content='\n'.join(['000,100 100,200 200,300', 'nine| ten| eleven'])
        ),
        DraftSrt(
            index=4,
            start=timedelta(0, 70, 100),
            end=timedelta(0, 80, 200),
            content='\n'.join(['000,100 100,200', 'twelve thirteen'])
        ),
        DraftSrt(
            index=5,
            start=timedelta(0, 90, 100),
            end=timedelta(0, 100, 200),
            content='\n'.join(['000,100 200,300', 'fourteen| fifteen'])
        ),
        DraftSrt(
            index=6,
            start=timedelta(0, 110, 100),
            end=timedelta(0, 120, 200),
            content='\n'.join(['000,100', 'sixteen'])
        )
    ]

    trans(subs, 33, lambda l: [str(len(_.split())) for _ in l])

    trans_subs = [
        DraftSrt(
            index=1,
            start=timedelta(0, 10, 100),
            end=timedelta(0, 20, 200),
            content='\n'.join([
                '000,100 100,200 200,300 300,400 400,500',
                'one two three| four five',
                '3|3'
            ])
        ),
        DraftSrt(
            index=2,
            start=timedelta(0, 30, 100),
            end=timedelta(0, 40, 200),
            content='\n'.join(['000,100 100,200 200,300', 'six| seven| eight|', '|1|1|'])
        ),
        DraftSrt(
            index=3,
            start=timedelta(0, 50, 100),
            end=timedelta(0, 60, 200),
            content='\n'.join(['000,100 100,200 200,300', 'nine| ten| eleven', '1|1|4'])
        ),
        DraftSrt(
            index=4,
            start=timedelta(0, 70, 100),
            end=timedelta(0, 80, 200),
            content='\n'.join(['000,100 100,200', 'twelve thirteen'])
        ),
        DraftSrt(
            index=5,
            start=timedelta(0, 90, 100),
            end=timedelta(0, 100, 200),
            content='\n'.join(['000,100 200,300', 'fourteen| fifteen', '|2'])
        ),
        DraftSrt(
            index=6,
            start=timedelta(0, 110, 100),
            end=timedelta(0, 120, 200),
            content='\n'.join(['000,100', 'sixteen'])
        )
    ]

    for i, sub in enumerate(subs):
        assert(sub == trans_subs[i])

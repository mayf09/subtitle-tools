import json

import click
import srt

from draft_srt import DraftSrt

from utils.res2draft import detail2srts


@click.group()
def subtool():
    pass


@subtool.command()
@click.option('-i', 'res_file', type=click.File('r'), required=True, help='音频文件')
@click.option('-o', 'draft_srt_file', type=click.File('w'), required=True, help='草稿字幕文件')
def res2draft(res_file, draft_srt_file):
    """
    从语音识别文件生成 .draft.srt 文件
    """
    res = json.load(res_file)
    result_detail = res['Data']['ResultDetail']
    draft_srts = []
    for detail in result_detail:
        srts = detail2srts(detail)
        draft_srts.extend(srts)

    srt.sort_and_reindex(draft_srts)
    draft_string = srt.compose(draft_srts)
    draft_srt_file.write(draft_string)
    draft_srt_file.flush()


@subtool.command()
@click.option('-i', required=True, help='源草稿字幕文件（英文）')
@click.option('-o', required=False, help='目标草稿字幕文件，如果不指定，输出到源文件')
def trans():
    """
    机器翻译 .draft.srt 文件
    """
    pass


@subtool.command()
@click.option('-i', required=True, help='源草稿字幕文件')
@click.option('-o', required=True, help='生成字幕文件')
@click.option('--langs', multiple=True, default=['en', 'zh'], required=False, help='指定生成字幕语言')
def draft2final():
    """
    使用 .draft.srt 文本生成最终字幕文件
    """
    pass


if __name__ == "__main__":
    subtool()

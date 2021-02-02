import json

import click
import srt

from draft_srt import DraftSrt

from utils.config import SubtoolConfig
from utils.get_asr_res import get_asr_res
from utils.res2draft import detail2srts
from utils.translate import translate_batch_text
from utils.trans_func import trans


@click.group()
def subtool():
    """
    字幕制作工具，使用自定义的草稿字幕（.draft.srt）
    """
    pass


@subtool.command()
@click.option('--secret-id', 'secret_id', type=str, required=False, help='云服务 SecretId')
@click.option('--secret-key', 'secret_key', type=str, required=False, help='云服务 SecretKey')
@click.option('--bucket-name', 'bucket_name', type=str, required=False, help='云服务桶名称')
def config(secret_id, secret_key, bucket_name):
    """
    配置参数
    """
    subtool_config = SubtoolConfig()
    if secret_id and secret_key:
        subtool_config.set_cloud_auth(secret_id, secret_key)
    if bucket_name:
        subtool_config.set_bucket_name(bucket_name)


@subtool.command()
@click.option('-i', 'audio_file', type=str, required=True, help='音频文件')
@click.option('-o', 'res_file', type=str, required=True, help='语音识别结果文件')
def audio2text(audio_file, res_file):
    """
    使用音频文件获得语音识别文件
    """
    get_asr_res(audio_file, res_file)


@subtool.command()
@click.option('-i', 'res_file', type=click.File('r'), required=True, help='语音识别结果文件')
@click.option('-o', 'draft_srt_file', type=click.File('w'), required=True, help='草稿字幕文件')
def text2draft(res_file, draft_srt_file):
    """
    使用语音识别文件生成 .draft.srt 文件
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
@click.option('-i', 'draft_srt_file', type=click.File('r+'), required=True, help='源草稿字幕文件（英文）')
def en2zh(draft_srt_file):
    """
    机器翻译 .draft.srt 文件（在原文件中添加翻译结果）
    """
    subs = srt.parse(draft_srt_file)
    subs = [_ for _ in subs]

    trans(subs, 2000, translate_batch_text, 0.2)

    draft_srt_file.seek(0)
    draft_srt_file.write(srt.compose(subs))
    draft_srt_file.flush()


@subtool.command()
@click.option('-i', 'draft_srt_file', type=click.File('r'), required=True, help='源草稿字幕文件')
@click.option('-o', 'final_srt_file', type=click.File('w'), required=True, help='生成字幕文件')
@click.option('--langs', 'langs', multiple=True, default=['en', 'zh'], required=False, help='指定生成字幕语言')
def draft2final(draft_srt_file, final_srt_file, langs):
    """
    使用 .draft.srt 文本生成最终字幕文件
    """
    srts = srt.parse(draft_srt_file)
    draft_srts = [DraftSrt.from_srt(_) for _ in srts]

    final_srts = []
    for _ in DraftSrt.to_final_srts(draft_srts, langs=langs):
        final_srts.append(_)

    for i in range(len(final_srts)):
        if len(final_srts[i].content) > 80:
            print(final_srts[i].to_srt())

    final_string = srt.compose(final_srts)

    final_srt_file.write(final_string)
    final_srt_file.flush()


if __name__ == "__main__":
    subtool()

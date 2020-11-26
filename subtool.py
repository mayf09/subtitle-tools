import click


@click.group()
def subtool():
    pass


@subtool.command()
@click.option('-i', required=True, help='音频文件')
@click.option('-o', required=False, help='草稿字幕文件')
@click.option('-k', type=bool, default=True, required=False, help='是否保留语音识别结果')
def audio2draft():
    """
    从音频文件生成 .draft.srt 文件
    """
    pass


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

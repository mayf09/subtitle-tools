from typing import List

import srt


TIME_OFFSET_INDEX=0
EN_INDEX=1
ZH_INDEX=2


class DraftSrt(srt.Subtitle):

    @property
    def time_offset(self) -> List[str]:
        return self.get_content_lines()[TIME_OFFSET_INDEX].split(' ')

    @property
    def en_text(self) -> str:
        if not self.has_en_text():
            return None
        return self.get_content_lines()[EN_INDEX]

    @en_text.setter
    def en_text(self, text: str):
        content_lines = self.get_content_lines()
        content_lines[EN_INDEX] = text
        self.content = '\n'.join(content_lines)

    @property
    def zh_text(self) -> str:
        if not self.has_zh_text():
            return None
        return self.get_content_lines()[ZH_INDEX]

    @zh_text.setter
    def zh_text(self, text: str):
        content_lines = self.get_content_lines()
        content_lines[ZH_INDEX] = text
        self.content = '\n'.join(content_lines)

    def get_content_lines(self) -> List[str]:
        return self.content.split('\n')

    def has_en_text(self) -> bool:
        return len(self.get_content_lines()) >= EN_INDEX + 1

    def has_zh_text(self) -> bool:
        return len(self.get_content_lines()) == ZH_INDEX + 1

    def check_time_offset(self) -> bool:
        if not self.has_en_text():
            return True
        return len(self.time_offset) == len(self.en_text.split())

    def check_zh_text(self) -> bool:
        # TODO:
        return True

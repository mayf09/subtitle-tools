from typing import Tuple
import configparser

from pathlib import Path


CONFIG_FILE = Path.home() / '.subtool.conf'


class SubtoolConfig:

    def __init__(self, config_file = CONFIG_FILE) -> None:

        self.config = configparser.ConfigParser()
        self.config_file = config_file

    def set_cloud_auth(self, secret_id: str, secret_key: str):

        self.config['tencentcloud'] = {}
        self.config['tencentcloud']['SecretId'] = secret_id
        self.config['tencentcloud']['SecretKey'] = secret_key
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def get_cloud_auth(self) -> Tuple[str, str]:

        self.config.read(self.config_file)
        # print(self.config.sections)  # DEBUG

        # 用户的账号信息
        # 获取方法： https://cloud.tencent.com/product/asr/getting-started

        secret_id = self.config['tencentcloud']['SecretId']
        secret_key = self.config['tencentcloud']['SecretKey']

        return secret_id, secret_key

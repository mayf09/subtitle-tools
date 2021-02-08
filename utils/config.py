from typing import Tuple
import configparser

from pathlib import Path


CONFIG_FILE = Path.home() / '.subtool.conf'


class SubtoolConfig:

    def __init__(self, config_file = CONFIG_FILE) -> None:

        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.get_config()

    def get_config(self):
        try:
            self.config.read(self.config_file)
        except Exception:
            pass

    def set_cloud_auth(self, secret_id: str, secret_key: str):

        if self.config.get('tencentcloud') is None:
            self.config['tencentcloud'] = {}
        self.config['tencentcloud']['SecretId'] = secret_id
        self.config['tencentcloud']['SecretKey'] = secret_key
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def get_cloud_auth(self) -> Tuple[str, str]:

        # print(self.config.sections)  # DEBUG

        # 用户的账号信息
        # 获取方法： https://cloud.tencent.com/product/asr/getting-started

        secret_id = self.config['tencentcloud']['SecretId']
        secret_key = self.config['tencentcloud']['SecretKey']

        return secret_id, secret_key

    def set_bucket_name(self, bucket_name: str):

        self.config['tencentcloud']['BucketName'] = bucket_name
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def get_bucket_name(self) -> str:

        return self.config['tencentcloud']['BucketName']

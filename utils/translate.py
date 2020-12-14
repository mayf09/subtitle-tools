import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

from utils.config import SubtoolConfig


def get_real_srt(subs):
    tmp = ''
    for sub in subs:
        en_text, time_text = sub.split('\n')
        if tmp == '':
            tmp = en_text
        else:
            tmp = ' '.join(tmp, en_text)
        while '|' in tmp:
            if tmp.split('|')[0].strip() != '':
                yield tmp.split('|')[0].strip()
            tmp = '|'.join(tmp[1:])


def translate_batch_text(text_list: list) -> list:
    print(text_list)
    print(sum([len(_) for _ in text_list]))
    try:
        subtool_config = SubtoolConfig()
        secret_id, secret_key = subtool_config.get_cloud_auth()
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

        req = models.TextTranslateBatchRequest()
        params = {
            "Source": "en",
            "Target": "zh",
            "ProjectId": 0,
            "SourceTextList": text_list,
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextTranslateBatch(req)
        print(resp.to_json_string())
        return resp.TargetTextList

    except TencentCloudSDKException as err:
        print(err)

import os
import sys
import time

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

from utils.config import SubtoolConfig

subtool_config = SubtoolConfig()
SecretId, SecretKey = subtool_config.get_cloud_auth()
BUCKET_NAME = subtool_config.get_bucket_name()


def upload_file(filePath):
    Key = os.path.basename(filePath)
    try:
        region = 'ap-shanghai'
        token = None
        scheme = 'https'
        config = CosConfig(Region=region, SecretId=SecretId, SecretKey=SecretKey, Token=token, Scheme=scheme)

        client = CosS3Client(config)

        response = client.upload_file(
            Bucket=BUCKET_NAME,
            LocalFilePath=filePath,
            Key=Key,
            PartSize=1,
            MAXThread=10,
            EnableMD5=False
        )
        # print(response)  # DEBUG
        print('upload file success.')

        Url = client.get_presigned_download_url(
            Bucket=BUCKET_NAME,
            Key=Key,
            Expired=300,
            Params={},
            Headers={}
        )
        # print(Url)  # DEBUG

        return Url
    except Exception as e:
        print(e)


def via_url(Url):
    """
    Url: https://asr-audio-1300466766.cos.ap-nanjing.myqcloud.com/test16k.wav
    """
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        clientProfile.signMethod = "TC3-HMAC-SHA256"
        client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

        req = models.CreateRecTaskRequest()
        params = { "ChannelNum": 1, "ResTextFormat" : 1, "SourceType" : 0 }
        req._deserialize(params)
        req.EngineModelType = "16k_en"
        req.Url = Url
        resp = client.CreateRecTask(req)
        print('create task success. {}'.format(resp.Data))
        return resp.Data.TaskId
    except TencentCloudSDKException as err:
        print(err)


def get_res(taskId):

    try:
        # print(taskId)  # DEBUG
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "ap-shanghai", clientProfile)

        req = models.DescribeTaskStatusRequest()
        params = { "TaskId": taskId }
        req._deserialize(params)

        resp = client.DescribeTaskStatus(req)
        # print(resp.to_json_string())
        return resp

    except TencentCloudSDKException as err:
        print(err)


def get_asr_res(audio_file, res_file):

    RESULT_FILE = res_file
    Url = upload_file(audio_file)
    taskId = via_url(Url)

    resp = get_res(taskId)
    while resp.Data.Status != 2:
        print('wait task complete.  {}'.format(resp.Data))
        time.sleep(5)
        resp = get_res(taskId)

    print('get res success.')
    print('write to {}.'.format(RESULT_FILE))
    with open(RESULT_FILE, 'w') as f:
        f.writelines(resp.to_json_string())

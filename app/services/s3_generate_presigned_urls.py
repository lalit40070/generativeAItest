import boto3
from botocore.client import BaseClient
from botocore.client import Config

from app.services.cloud_front_signing_helper import CloudFrontUtil
from app.core.settings.app import AppSettings
from app.core.config import get_app_settings

SETTINGS = get_app_settings()

def gen_pre_signed_url(url:str, s3client):
    object_id = url.replace("s3://{}/".format(str(SETTINGS.bucket_name)), '')
    pre_signed_url = s3client.generate_presigned_url('get_object', 
                                                    Params = {'Bucket': SETTINGS.bucket_name, 'Key': object_id}, 
                                                    ExpiresIn = 100)
    return pre_signed_url


def gen_pre_signed_url_from_key(key:str, s3client):
    pre_signed_url = s3client.generate_presigned_url('get_object', 
                                                    Params = {'Bucket': SETTINGS.bucket_name, 'Key': key}, 
                                                    ExpiresIn = 100)
    return pre_signed_url


def gen_cloud_front_url(url:str):
    object_id = url.replace("s3://{}/".format(str(SETTINGS.bucket_name)), '')
    cloud_front_url = "{}/{}".format(SETTINGS.cloud_front_url, object_id)
    cloud_front_util = CloudFrontUtil()
    signed_url = cloud_front_util.generate_presigned_url(cloud_front_url)
    return signed_url

def gen_cloud_front_url_from_key(key:str):
    cloud_front_url = "{}/{}".format(SETTINGS.cloud_front_url, key)
    cloud_front_util = CloudFrontUtil()
    signed_url = cloud_front_util.generate_presigned_url(cloud_front_url)
    return signed_url
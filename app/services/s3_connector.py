import boto3
from botocore.client import BaseClient, Config

from app.core.settings.app import AppSettings
from app.core.config import get_app_settings

SETTINGS = get_app_settings()


def s3_connector() -> BaseClient:
    s3 = boto3.client(service_name='s3', aws_access_key_id=SETTINGS.s3_access_key,
                      aws_secret_access_key=SETTINGS.s3_access_secret,config=Config(signature_version='s3v4'),
                      region_name=SETTINGS.s3_region
                      )

    return s3
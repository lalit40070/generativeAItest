import boto3
from botocore.client import BaseClient
from botocore.client import Config


from app.core.settings.app import AppSettings
from app.core.config import get_app_settings
import boto3



SETTINGS = get_app_settings()

def get_all_images(s3client, folder, images_url):
    s3 = boto3.resource('s3', aws_access_key_id=SETTINGS.s3_access_key,
         aws_secret_access_key= SETTINGS.s3_access_secret)
    bucket = s3.Bucket(SETTINGS.bucket_name)
    folder = SETTINGS.s3_avatar_folder if folder == "avatar" else SETTINGS.s3_selfies_folder
    prefix = "{}/{}".format(folder, images_url.split('/')[-2])
    return [object_summary.key for object_summary in bucket.objects.filter(Prefix=prefix)]


def delete_user_selfies(folder, user, purchase):
    s3 = boto3.resource('s3', aws_access_key_id=SETTINGS.s3_access_key,
         aws_secret_access_key= SETTINGS.s3_access_secret)
    bucket = s3.Bucket(SETTINGS.bucket_name)
    folder = SETTINGS.s3_avatar_folder if folder == "avatar" else SETTINGS.s3_selfies_folder

    """Adding 0 as selfie type is default 0 """
    prefix = "{}/{}_{}_{}".format(folder,user, purchase, 0)
    bucket.objects.filter(Prefix=prefix).delete()
import logging

from botocore.exceptions import ClientError
from app.core.settings.app import AppSettings
from app.core.config import get_app_settings

SETTINGS = get_app_settings()

def upload_file_to_bucket(s3_client, files, user_id, _type, purchase, style_id):
    s3_folder = SETTINGS.s3_avatar_folder if _type.toString() == "avatar" else SETTINGS.s3_selfies_folder
    base_image_path = "{}/{}_{}_{}".format(s3_folder, user_id, purchase, style_id)
    for i, image in enumerate(files):
        file_name = "{}({}).{}".format(user_id, i, image.content_type.split('/')[1])
        try:
            response = s3_client.upload_fileobj(image.file, SETTINGS.bucket_name, f"{base_image_path}/{file_name}")
        except ClientError as e:
            logging.error(e)
            return False
    upload_url = "s3://{}/{}/".format(SETTINGS.bucket_name, base_image_path)
    return upload_url
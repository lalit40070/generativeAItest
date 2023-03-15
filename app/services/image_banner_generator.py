import sys
import boto3
import logging


from botocore.exceptions import ClientError
from PIL import Image
from io import BytesIO
from app.core.config import get_app_settings
from .s3_generate_presigned_urls import gen_pre_signed_url_from_key, gen_cloud_front_url_from_key


SETTINGS = get_app_settings()

def create_banner(s3_client, images: list, purchase: int, user:str):

    

    s3 = boto3.resource('s3', aws_access_key_id=SETTINGS.s3_access_key,
         aws_secret_access_key= SETTINGS.s3_access_secret)
    bucket = s3.Bucket(SETTINGS.bucket_name)

    """ Check if banner is already created and returing existing banner"""

    base_image_path = "{}/{}_{}".format(SETTINGS.s3_avatar_folder, user, purchase)

    if len([o for o in bucket.objects.filter(Prefix=f"{base_image_path}/banner.jpg")]) > 0:
        return gen_cloud_front_url_from_key(f"{base_image_path}/banner.jpg")

    """ Creating banner image code"""
    image_keys = get_keys_from_s3_url(images, bucket)
    images = [Image.open(BytesIO(bucket.Object(image).get().get('Body').read())) for image in image_keys[:3]]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    in_mem_file = BytesIO()
    new_im.save(in_mem_file, format='png')
    in_mem_file.seek(0)


    """ uploading to S3"""
    try:
        response = s3_client.upload_fileobj(in_mem_file, SETTINGS.bucket_name, f"{base_image_path}/banner.jpg")
    except ClientError as e:
        logging.error(e)
        return False

    """ generating presigned url for mobile app access"""
    presigned_url = gen_cloud_front_url_from_key(f"{base_image_path}/banner.jpg")
    return presigned_url


def get_keys_from_s3_url(urls:list, bucket:str):
    prefixs = [url.replace("s3://{}/".format(SETTINGS.bucket_name), "") for url in urls]
    object_keys = []
    for prefix in prefixs:
        object_key = [object_summary.key for object_summary in bucket.objects.filter(Prefix=prefix)]
        object_keys = object_keys + object_key 
    
    return object_keys
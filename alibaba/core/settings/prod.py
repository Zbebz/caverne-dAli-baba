from .base import *

DEBUG = False

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = "eu-central-2"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.amazonaws.com"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# s3 static settings
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# s3 public media settings
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}


STORAGES = {
    "default": {
        "BACKEND": "core.settings.storages.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "core.settings.storages.StaticStorage",
    },
}

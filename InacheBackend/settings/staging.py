from .base import *

print("test: i am inside the staging.py file")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "inache_stage",
        "USER": "postgres",
        "PASSWORD": "admin98",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
AWS_S3_ACCESS_KEY_ID = "AKIAUL4AWPROFODPDKF5"
AWS_S3_SECRET_ACCESS_KEY = "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"
AWS_S3_BUCKET_NAME = "inache-attachments-stage"
AWS_S3_REGION_NAME = "ap-south-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "private"
AWS_PRESIGNED_EXPIRY = 5000

FILE_UPLOAD_STORAGE = "local"

if FILE_UPLOAD_STORAGE == "local":
    MEDIA_ROOT_NAME = "media"
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

if FILE_UPLOAD_STORAGE == "s3":
    DEFAULT_FILE_STORAGE = ('storages.backends.s3boto3.S3Boto3Storage')

CRONTAB_DJANGO_SETTINGS_MODULE="InacheBackend.settings.staging"
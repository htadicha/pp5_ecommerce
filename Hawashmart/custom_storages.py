"""
Custom storage classes for AWS S3.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files (product images, user uploads).
    Ensures files are publicly readable.
    """
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


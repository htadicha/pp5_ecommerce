"""
Custom storage classes for AWS S3.
"""

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files (product images, user uploads).
    Ensures files are publicly readable.
    """

    location = "media"
    default_acl = "public-read"
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        """
        Initialize storage with explicit settings.
        """
        # Override default_acl before calling super
        kwargs.setdefault("default_acl", "public-read")
        super().__init__(*args, **kwargs)
        # Ensure default_acl is set even after initialization
        self.default_acl = "public-read"

    def url(self, name):
        """
        Override url to ensure it returns the correct public URL without query strings.
        """
        url = super().url(name)
        # Remove query string authentication if present
        if "?" in url:
            url = url.split("?")[0]
        return url

    def _save(self, name, content):
        """
        Override _save to ensure ACL is applied correctly.
        """
        # Ensure ACL is set for this save operation
        self.default_acl = "public-read"
        return super()._save(name, content)

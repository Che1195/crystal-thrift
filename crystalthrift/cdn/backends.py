from storages.backends.s3boto3 import S3Boto3Storage

class StaticRoots3Boto3Storage(S3Boto3Storage):
    location = 'static'

class MediaRoots3Boto3Storage(S3Boto3Storage):
    location = 'media'
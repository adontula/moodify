import boto3
from botocore.client import Config
import requests

s3 = boto3.resource('s3')

data = open('face.jpg', 'rb')
s3.Bucket('azureemotion992').put_object(Key='face.jpg', Body = data)

import boto.s3
conn = boto.s3.connect_to_region('us-east-2')  # or region of choice
bucket = conn.get_bucket('azureemotion992')
key = bucket.lookup('face.jpg')
key.set_acl('public-read')

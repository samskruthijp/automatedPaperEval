import os, io
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format
from google.cloud.vision import types

mime_type = 'application/pdf'

batch_size = 2


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

client = vision.ImageAnnotatorClient()

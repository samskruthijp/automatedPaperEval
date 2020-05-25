import re
import os, io
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision.ImageAnnotatorClient()

FOLDER_PATH = r'C:/Users/Shivani T Eswara/finyear/visionapi/images'
IMAGE_FILE = 'house sketch.jpeg'
FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

with io.open(FILE_PATH, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.document_text_detection(image=image,
    image_context={"language_hints": ["en"]},)

docText = response.full_text_annotation.text
print(docText)

import os, io
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision.ImageAnnotatorClient()

file_name='house sketch.jpeg'
image_path=os.path.join('.\images',file_name)

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.web_detection(image=image)
web_detection = response.web_detection

#print(web_detection)
label = (web_detection.best_guess_labels)
print(type(label))

for entity in web_detection.web_entities:
    print(entity.description)
    print(entity.score)
    print('-'*50)



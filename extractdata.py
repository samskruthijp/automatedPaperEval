from google.cloud import storage
import json
import os, io
from pprint import pprint

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'


storage_client = storage.Client()
bucket = storage_client.get_bucket('paperevaluation')
blob=bucket.blob('pdf_result output-1-to-2.json')

data = json.loads(blob.download_as_string(client=None))

answer_file = open("Extracted.txt", "a",encoding="utf-8")

print(type(data))
print(len(data['responses']))
for i in range(1, len(data['responses'])):
    answer = data['responses'][i]['fullTextAnnotation']['text']
    answer_file.write(answer)
    
#answer = data['responses'][0]['fullTextAnnotation']['text'] 
answer_file.close()
print("done")
#print(answer)
"""
answer_file = open("Extracted.txt", "w",encoding="utf-8")
answer_file.write(answer)
answer_file.close()
print("done")

#print(answer)
"""

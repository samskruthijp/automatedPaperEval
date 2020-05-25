
"""OCR with PDF/TIFF as source files on GCS"""
import re
import os, io
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
batch_size = 2

client = vision.ImageAnnotatorClient()

feature = vision.types.Feature(
    type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

gcs_source_uri='gs://paperevaluation/IoT assignment.pdf'
gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
input_config = vision.types.InputConfig(
    gcs_source=gcs_source, mime_type=mime_type)

gcs_destination_uri='gs://paperevaluation/pdf_result '
gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
output_config = vision.types.OutputConfig(
    gcs_destination=gcs_destination, batch_size=batch_size)

async_request = vision.types.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config,
    output_config=output_config)

operation = client.async_batch_annotate_files(
    requests=[async_request])

print('Waiting for the operation to finish.')
operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
storage_client = storage.Client()

match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
bucket_name = match.group(1)
prefix = match.group(2)

bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
blob_list = list(bucket.list_blobs(prefix=prefix))
print('Output files:')
for blob in blob_list:
    print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
answer_file = open ("Extractedsolution.txt", "a",encoding="utf-8")
for i in range(0, len(blob_list)):
    output = blob_list[i]

    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())

    # The actual response for the first page of the input file.
    for j in range(0, len(response.responses)):

        page_response = response.responses[j]
        annotation = page_response.full_text_annotation

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
        answer_file.write(annotation.text)
        #print(u'Full text:\n{}'.format( annotation.text))
answer_file.close()
print("finished writing to file")
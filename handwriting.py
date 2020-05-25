import re
import os, io
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

def upload_file(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def detect_document(gcs_source_uri, gcs_destination_uri):
    mime_type = 'application/pdf'
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    print("bucket name is "+bucket_name)
    print("prefix is "+prefix)
    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print(blob_list)
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    answer_file = open ("Oksolution.txt", "a",encoding="utf-8")
    for i in range(0, len(blob_list)):
        output = blob_list[i]

        json_string = output.download_as_string()
        response = json_format.Parse(
            json_string, vision.types.AnnotateFileResponse())


        for j in range(0, len(response.responses)):

            page_response = response.responses[j]
            annotation = page_response.full_text_annotation
            answer_file.write(annotation.text)
        
    answer_file.close()
    print("finished writing to file")


upload_file('paperevaluation', 'C:/Users/Shivani T Eswara/finyear/visionapi/uploaded files/ok.pdf', 'ok_solution_gcp.pdf')
detect_document('gs://paperevaluation/ok_solution_gcp.pdf', 'gs://paperevaluation/ok_result ')






import os, io
from google.cloud import vision
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

bucket_name = 'paperevaluation'
source_file_name = 'C:/Users/Shivani T Eswara/finyear/visionapi/uploaded files/demo solution.pdf'
destination_blob_name = 'demo_solution_gcp.pdf'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)

blob.upload_from_filename(source_file_name)

print(
    "File {} uploaded to {}.".format(
        source_file_name, destination_blob_name
    )
)
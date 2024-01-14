import boto3
import json
import base64
import os
import io
from const import *
from utils import *

file_storage_bucket = os.environ['FILE_STORAGE_BUCKET']

def upload_file(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE

    # Extract the file content and file name
    file_content = event['body']
    file_content = base64.b64decode(file_content)

    # Validate if the file's size is less than the limit
    if len(file_content) > FILE_SIZE_LIMIT:
        return FILE_TOO_LARGE_RESPONSE
    
    file_content = io.BytesIO(file_content)
    file_key = event['queryStringParameters']['file_key']

    # Initialize the S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file to S3
        s3.upload_fileobj(file_content, Bucket=file_storage_bucket, Key=f'{user_id}/{file_key}')
        return UPLOAD_SUCCESS_RESPONSE
    except Exception as e:
        return server_error_response(str(e))
    
def get_presigned_url(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE
    
    file_key = event['queryStringParameters']['file_key']

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Generate a presigned URL for the file
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': file_storage_bucket, 'Key': f'{user_id}/{file_key}'},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return presigned_url_response(presigned_url)
    except Exception as e:
        return server_error_response(str(e))
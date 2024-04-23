import boto3
import json
import base64
import os
import io
from const import *
from utils import *

secret = get_secret()

jwt_secret = secret.get('JWT_SECRET')
service_key = secret.get('SERVICE_KEY')
file_storage_bucket = secret.get('FILE_STORAGE_BUCKET')

def upload_file(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event, jwt_secret)
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
        return success_response('File uploaded successfully')
    except Exception as e:
        return server_error_response(str(e))
    
def get_presigned_url(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event, jwt_secret)
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
    
def delete_file(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event, jwt_secret)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE
    
    file_key = event['queryStringParameters']['file_key']

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Delete the file from S3
    try:
        s3.delete_object(Bucket=file_storage_bucket, Key=f'{user_id}/{file_key}')
        return success_response('File deleted successfully')
    except Exception as e:
        return server_error_response(str(e))
    
def create_folder(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event, jwt_secret)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE
    
    path = event['queryStringParameters']['path']

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Create a folder in S3
    try:
        s3.put_object(Bucket=file_storage_bucket, Key=f'{user_id}/{path}')
        return success_response('Folder created successfully')
    except Exception as e:
        return server_error_response(str(e))
    
def get_files(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the user
    try:
        user_id = authenticate(event, jwt_secret)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE
    
    # Initialize the S3 client
    s3 = boto3.client('s3')
    path = event['queryStringParameters']['path']
    prefix = f'{user_id}/{path}'

    # Get the list of files/directories from S3 at a specific path (not recursive)
    try:
        response = s3.list_objects_v2(Bucket=file_storage_bucket, Prefix=prefix)
        if 'Contents' not in response:
            return list_files_response([])

        files = []
        for file in response['Contents']:
            no_prefix_file_key = file['Key'].replace(prefix, '')
            if '/' in no_prefix_file_key:
                to_append = no_prefix_file_key.split('/')[0] + '/'
                if to_append not in files:
                    files.append(to_append)
            else:
                files.append(no_prefix_file_key)
        return list_files_response(files)
    except Exception as e:
        print(f'Error: {e}')
        return server_error_response(str(e)) 
    
def robot_upload_file(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the robot
    try:
        authenticate_robot(event, service_key)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE
    
    user_id = event['queryStringParameters']['user_id']

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
        s3.put_object(Bucket=file_storage_bucket, Key=f'{user_id}/{file_key}', Body=file_content, Tagging='created-by=robot')
        return success_response('File uploaded successfully')
    except Exception as e:
        print(f'Error: {e}')
        return server_error_response(str(e))
    
def robot_get_presigned_url(event, context):
    print(f'Event headers: {event["headers"]}')

    # Authenticate the robot
    try:
        authenticate_robot(event, service_key)
    except Exception as e:
        return UNAUTHORIZED_RESPONSE
    
    user_id = event['queryStringParameters']['user_id']
    file_path = event['queryStringParameters']['file_path']

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Generate a presigned URL for the file
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': file_storage_bucket, 'Key': f'{user_id}/{file_path}'},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return presigned_url_response(presigned_url)
    except Exception as e:
        print(f'Error: {e}')
        return server_error_response(str(e))

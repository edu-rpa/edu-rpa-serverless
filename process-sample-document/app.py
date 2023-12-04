import json
import boto3
import cv2

from transform import perspective_transform


def process_sample_document(event, context):
    # Load the image from the S3 bucket
    s3 = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    document_key = event['Records'][0]['s3']['object']['key']

    # Set up path
    tmpkey = document_key.replace('/', '')
    download_path = '/tmp/{}'.format(tmpkey)
    upload_path = '/tmp/{}-processed'.format(tmpkey)

    s3.download_file(bucket_name, document_key, download_path)
    image = cv2.imread(download_path)

    # Perform perspective transformation
    document = perspective_transform(image)

    # Save the processed image to the local filesystem
    cv2.imwrite(upload_path, document)

    # Save the processed image to the S3 bucket
    processed_key = document_key.replace('original', 'processed')
    s3.upload_file(upload_path, bucket_name, processed_key)

    # Return the processed image URL
    processed_url = f'https://{bucket_name}.s3.amazonaws.com/{processed_key}'
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed_url': processed_url
        })
    }

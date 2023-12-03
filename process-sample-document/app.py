import json
import boto3

from transform import perspective_transform


def process_sample_document(event, context):
    # Load the image from the S3 bucket
    s3 = boto3.resource('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    document_key = event['Records'][0]['s3']['object']['key']
    document_object = s3.get_object(Bucket=bucket_name, Key=document_key)
    document_bytes = document_object['Body'].read()

    # Perform perspective transformation
    document = perspective_transform(document_bytes)

    # Save the processed image to the S3 bucket
    processed_key = document_key.replace('original', 'processed')
    s3.put_object(Bucket=bucket_name, Key=processed_key, Body=document)

    # Return the processed image URL
    processed_url = f'https://{bucket_name}.s3.amazonaws.com/{processed_key}'
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed_url': processed_url
        })
    }

import json
import boto3
import cv2
import numpy as np

from transform import perspective_transform


def upload_sample_document(event, context):
    # Get file from POST request
    file_content = event['body'].encode('utf-8')

    # Convert the file content to a numpy array
    np_array = np.fromstring(file_content, np.uint8)
    
    # Convert numpy array to image
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Perform perspective transformation
    document = perspective_transform(image)

    # Get id from path parameters
    id = event['pathParameters']['id']
    upload_path = f'/tmp/{id}-processed'

    # Save the processed image to the local filesystem
    cv2.imwrite(upload_path, document)

    # Save the processed image to the S3 bucket
    processed_key = f'{id}-processed.jpg'
    bucket_name = 'edurpa-document-template'
    s3.upload_file(upload_path, bucket_name, processed_key)

    # Return the processed image URL
    processed_url = f'https://{bucket_name}.s3.amazonaws.com/{processed_key}'
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed_url': processed_url
        })
    }

import base64
import json
import boto3
import cv2
import numpy as np

from transform import perspective_transform, resize_image


def upload_sample_document(event, context):
    print(f'Event headers: {event["headers"]}')

    # Get file from POST request
    file_content = event['body']

    # Decode the base64 string
    decoded_image = base64.b64decode(file_content)

    # Convert the bytes to a numpy array
    np_array = np.fromstring(decoded_image, np.uint8)

    # Read the image using OpenCV
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    print(f'Image shape: {image.shape}')

    width = int(event['queryStringParameters']['width'])
    height = int(event['queryStringParameters']['height'])

    if event['queryStringParameters']['isScanned'] == 'false':
        # Perform perspective transformation
        document = perspective_transform(image, [width, height])
    else:
        document = resize_image(image, [width, height])

    # Get id from path parameters
    id = event['pathParameters']['id']
    upload_path = f'/tmp/{id}-processed.jpg'

    # Save the processed image to the local filesystem
    cv2.imwrite(upload_path, document)

    # Save the processed image to the S3 bucket
    processed_key = f'{id}-processed.jpg'
    bucket_name = 'edurpa-document-template'
    s3 = boto3.client('s3')
    s3.upload_file(upload_path, bucket_name, processed_key)

    # Generate a presigned URL for the uploaded file
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': processed_key},
        ExpiresIn=3600  # URL expires in 1 hour
    )

    # Return the presigned URL
    return {
        'statusCode': 200,
        'body': json.dumps({
            'url': presigned_url
        })
    }

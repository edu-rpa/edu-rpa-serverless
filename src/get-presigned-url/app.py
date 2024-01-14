import json
import boto3

def get_presigned_url_handler(event, context):
    # Get id from path parameters
    id = event['pathParameters']['id']
    processed_key = f'{id}-processed.jpg'
    bucket_name = 'edurpa-document-template'
    s3 = boto3.client('s3')

    # Generate a presigned URL for the file
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

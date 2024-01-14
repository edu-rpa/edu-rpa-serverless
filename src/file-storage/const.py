import json

UNAUTHORIZED_RESPONSE = {
    'statusCode': 401,
    'body': json.dumps('Unauthorized')
}

FILE_TOO_LARGE_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('File size is too large')
}

UPLOAD_SUCCESS_RESPONSE = {
    'statusCode': 200,
    'body': json.dumps('File uploaded successfully')
}

SERVER_ERROR_RESPONSE = {
    'statusCode': 500,
    'body': json.dumps('Internal server error')
}

def server_error_response(message):
    return {
        'statusCode': 500,
        'body': json.dumps(message)
    }

def presigned_url_response(url):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'url': url
        })
    }

FILE_SIZE_LIMIT = 100000000
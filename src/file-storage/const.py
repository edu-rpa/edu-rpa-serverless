import json

UNAUTHORIZED_RESPONSE = {
    'statusCode': 401,
    'body': json.dumps('Unauthorized')
}

FILE_TOO_LARGE_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('File size is too large')
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

def success_response(message):
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }

def list_files_response(files):
    return {
        'statusCode': 200,
        'body': json.dumps(files)
    }

FILE_SIZE_LIMIT = 100000000
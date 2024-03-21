import json
import os
import jwt
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "edu-rpa/dev/secrets"
    region_name = "ap-southeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def validate_token(token, jwt_secret):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    
def authenticate(event, jwt_secret):
    # Extract the authorization header
    try:
        auth_header = event['headers']['authorization']
    except KeyError:
        auth_header = event['headers']['Authorization']
    if not auth_header:
        raise Exception('Unauthorized')

    token = auth_header.split(' ')[1]  # Bearer token
    payload = validate_token(token, jwt_secret)

    # Validate the token and get the user id
    if not payload:
        raise Exception('Unauthorized')
    user_id = payload['id']
    return user_id
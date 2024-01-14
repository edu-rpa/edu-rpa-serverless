import os
import jwt

def validate_token(token):
    secret = os.environ['JWT_SECRET']
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    
def authenticate(event):
    # Extract the authorization header
    try:
        auth_header = event['headers']['authorization']
    except KeyError:
        auth_header = event['headers']['Authorization']
    if not auth_header:
        raise Exception('Unauthorized')

    token = auth_header.split(' ')[1]  # Bearer token
    payload = validate_token(token)

    # Validate the token and get the user id
    if not payload:
        raise Exception('Unauthorized')
    user_id = payload['id']
    return user_id
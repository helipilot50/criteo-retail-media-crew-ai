import requests
import time
import os

TOKEN_CACHE = {
    'token': None,
    'expires_at': 0
}

def get_token():
    current_time = int(time.time())
    
    if TOKEN_CACHE['token'] is None or TOKEN_CACHE['expires_at'] <= current_time:
        
        clientId = os.environ["CRITEO_CLIENT_ID"]
        clientSecret = os.environ["CRITEO_CLIENT_SECRET"]
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": clientId,
            "client_secret": clientSecret,
            "grant_type": "client_credentials",
        }
        response = requests.post('https://api.criteo.com/oauth2/token', headers=headers, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            TOKEN_CACHE['token'] = token_data['access_token']
            TOKEN_CACHE['expires_at'] = current_time + token_data['expires_in']
        else:
            raise Exception('Failed to fetch access token')
    
    return TOKEN_CACHE['token']
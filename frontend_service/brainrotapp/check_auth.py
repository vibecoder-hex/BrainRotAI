import requests

def is_authenticate(access_token):
    if access_token:
        try:
            response = requests.get('http://127.0.0.1:8001/api/users/me', cookies={'access_token': access_token})
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            return False
    return False
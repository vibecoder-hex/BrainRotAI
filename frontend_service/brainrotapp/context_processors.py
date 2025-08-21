import requests

def auth_context(request):
    access_token = request.COOKIES.get("access_token")
    if access_token:
        try:
            response = requests.get("http://127.0.0.1:8001/api/users/me", cookies={"access_token": access_token})
            if response.status_code == 200:
                return {"is_auth": True}
            else:
                return {"is_auth": False}
        except requests.exceptions.RequestException:
            return {"is_auth": False}
    else:
        return {"is_auth": False}
            
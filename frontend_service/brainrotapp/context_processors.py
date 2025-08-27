from .check_auth import is_authenticate

def auth_context(request):
    access_token = request.COOKIES.get("access_token")
    if is_authenticate(access_token):
        return {"is_auth": True}
    return {"is_auth": False}
            
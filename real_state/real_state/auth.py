from fastapi import HTTPException, Request
from users.models import User


def check_exists_user(user_id):
    exists_user = User.objects.filter(id=user_id).exists()
    return exists_user


def is_logged(request: Request):
    cookies = request.cookies
    user_id = cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged")

    if not check_exists_user(user_id):
        raise HTTPException(status_code=401, detail="Not logged")

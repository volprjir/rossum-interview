import secrets
from http.client import HTTPException

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import settings

security = HTTPBasic()


class AuthorizationService:
    @staticmethod
    def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
        correct_username = settings.basic_auth_username
        correct_password = settings.basic_auth_password.get_secret_value()
        current_username_bytes = credentials.username.encode("utf8")
        current_password_bytes = credentials.password.encode("utf8")

        if not correct_username or not correct_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error",
            )
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password.encode("utf8")
        )

        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username.encode("utf8")
        )

        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

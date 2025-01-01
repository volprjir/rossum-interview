import pytest
from fastapi import HTTPException, status

from config import settings
from services.authorization_service import AuthorizationService


def verify_credentials(credentials):
    return AuthorizationService.verify_credentials(credentials)


def test_verify_credentials_success(valid_credentials):
    assert verify_credentials(valid_credentials) is None


def test_verify_credentials_invalid_username(invalid_credentials):
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(invalid_credentials)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect username or password"


def test_verify_credentials_invalid_password(valid_credentials, monkeypatch):
    monkeypatch.setattr(valid_credentials, "password", "invalid")
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(valid_credentials)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect username or password"


def test_verify_credentials_missing_username(valid_credentials, monkeypatch):
    monkeypatch.setattr(settings, "basic_auth_username", None)
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(valid_credentials)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Server configuration error"


def test_verify_credentials_missing_password(valid_credentials, monkeypatch):
    monkeypatch.setattr(settings.basic_auth_password, "get_secret_value", lambda: None)
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(valid_credentials)
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Server configuration error"

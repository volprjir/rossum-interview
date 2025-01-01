import os

import pytest
from fastapi.security import HTTPBasicCredentials

from config import settings
from services.postbin_service import PostbinService
from services.rossum_service import RossumService


@pytest.fixture
def mock_requests_post(mocker):
    return mocker.patch("requests.post")


@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")



@pytest.fixture
def raw_xml():
    with open(os.path.join(os.path.dirname(__file__), 'test_data', 'input.xml')) as file:
        return file.read()

@pytest.fixture
def expected_xml():
    with open(os.path.join(os.path.dirname(__file__), 'test_data', 'expected_output.xml')) as file:
        return file.read()

@pytest.fixture
def mock_rossum_service(mocker, raw_xml):
    mocker.patch.object(RossumService, "export_queue", return_value=raw_xml)


@pytest.fixture
def mock_postbin_service(mocker):
    mock_send_data = mocker.patch.object(PostbinService, "send_data")
    return mock_send_data


@pytest.fixture
def valid_credentials():
    return HTTPBasicCredentials(
        username=settings.basic_auth_username,
        password=settings.basic_auth_password.get_secret_value(),
    )


@pytest.fixture
def invalid_credentials():
    return HTTPBasicCredentials(username="invalid", password="invalid")

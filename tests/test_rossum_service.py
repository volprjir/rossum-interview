import pytest
from requests.exceptions import HTTPError
from services.rossum_service import RossumService
from exceptions.rossum import RossumExportError, RossumLoginError


def test_token_success(mock_requests_post):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {"key": "fake_token"}
    service = RossumService()
    assert service.token == "fake_token"

def test_token_http_error(mock_requests_post):
    mock_requests_post.return_value.raise_for_status.side_effect = HTTPError("HTTP Error")
    service = RossumService()
    with pytest.raises(RossumLoginError):
        service.token

def test_export_queue_success(mock_requests_get, mocker):
    mocker.patch.object(RossumService, 'token', new_callable=mocker.PropertyMock, return_value="fake_token")
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.text = "<xml>data</xml>"
    service = RossumService()
    result = service.export_queue("queue_id", "annotation_id")
    assert result == "<xml>data</xml>"

def test_export_queue_http_error(mock_requests_get, mocker):
    mocker.patch.object(RossumService, 'token', new_callable=mocker.PropertyMock, return_value="fake_token")
    mock_requests_get.return_value.raise_for_status.side_effect = HTTPError("HTTP Error")
    service = RossumService()
    with pytest.raises(RossumExportError):
        service.export_queue("queue_id", "annotation_id")
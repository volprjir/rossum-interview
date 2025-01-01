import pytest
from requests.exceptions import HTTPError

from config import settings
from services.postbin_service import PostbinService


def test_send_data_success(mock_requests_post):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.raise_for_status.return_value = None
    PostbinService.send_data("12345")
    mock_requests_post.assert_called_once_with(
        url=settings.postbin_url,
        json={"annotationId": "12345"}
    )

def test_send_data_http_error(mock_requests_post):
    mock_requests_post.return_value.raise_for_status.side_effect = HTTPError("HTTP Error")
    with pytest.raises(HTTPError):
        PostbinService.send_data("12345")

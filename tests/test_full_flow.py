import base64
import os

import xmltodict
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_export_endpoint_unauthorized(mock_rossum_service):
    body = {"annotation_id": "12345", "queue_id": "67890"}

    response = client.post(url="/export", json=body)
    assert response.status_code == 401


def test_export_endpoint_bad_request(mock_rossum_service):
    body = {
        "annotation_id": "12345"
        # Missing "queue_id"
    }

    response = client.post(
        url="/export",
        json=body,
        auth=(os.getenv("BASIC_AUTH_USERNAME"), os.getenv("BASIC_AUTH_PASSWORD")),
    )
    assert response.status_code == 422


def test_export_endpoint_bad_request_extra_parameter(mock_rossum_service):
    body = {
        "annotation_id": "12345",
        "queue_id": "67890",
        "extra_param": "extra_value",
    }

    response = client.post(
        url="/export",
        json=body,
        auth=(os.getenv("BASIC_AUTH_USERNAME"), os.getenv("BASIC_AUTH_PASSWORD")),
    )
    assert response.status_code == 422


def test_export_endpoint(mock_rossum_service, mock_postbin_service, expected_xml):
    body = {"annotation_id": "12345", "queue_id": "67890"}

    response = client.post(
        url="/export",
        json=body,
        auth=(os.getenv("BASIC_AUTH_USERNAME"), os.getenv("BASIC_AUTH_PASSWORD")),
    )
    mock_postbin_service.assert_called_once()
    sent_data = mock_postbin_service.call_args[0][0]

    decoded_result = base64.b64decode(sent_data).decode()
    result_dict = xmltodict.parse(decoded_result)
    expected_dict = xmltodict.parse(expected_xml)
    assert result_dict == expected_dict
    assert response.status_code == 200
    assert response.json() == {"success": True}

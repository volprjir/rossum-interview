import requests

from config import settings
from exceptions.rossum import RossumExportError, RossumLoginError


class RossumService:
    @property
    def token(self):
        try:
            payload = {
                "username": settings.rossum_username,
                "password": settings.rossum_password.get_secret_value(),
            }
            response = requests.post(f"{settings.rossum_api}/auth/login", json=payload)
            response.raise_for_status()

            return response.json()["key"]
        except requests.exceptions.HTTPError as e:
            raise RossumLoginError("Failed to login to Rossum API")

    def export_queue(
        self, queue_id: str, annotation_id: str, export_format: str = "xml"
    ) -> str:
        try:
            headers = {"Authorization": f"Bearer {self.token}"}

            query_parameters = {"id": annotation_id, "format": export_format}

            response = requests.get(
                f"{settings.rossum_api}/queues/{queue_id}/export",
                headers=headers,
                params=query_parameters,
            )
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            raise RossumExportError("Failed to export data from Rossum API")

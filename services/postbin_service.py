import requests

from config import settings


class PostbinService:
    @staticmethod
    def send_data(annotation_id: str):
        payload = {"annotationId": annotation_id}
        response = requests.post(url=settings.postbin_url, json=payload)
        response.raise_for_status()

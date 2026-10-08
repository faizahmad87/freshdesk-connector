import base64

from app.config import Config


class FreshdeskAuth:
    @staticmethod
    def get_auth_header() -> dict[str, str]:
        token = base64.b64encode(f"{Config.FRESHDESK_API_KEY}:X".encode()).decode()
        return {"Authorization": f"Basic {token}"}

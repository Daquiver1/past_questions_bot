"""Api module for the project."""
import requests


class BackendClient:
    """Client for the backend API."""

    def __init__(self, base_url: str) -> None:
        """Initialize the client."""
        self.base_url = base_url

    async def register_new_user(self, json: dict) -> dict:
        """Send a POST request to the specified endpoint."""
        try:
            response = requests.post(f"{self.base_url}/user", json=json)
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
            }

    async def get_user_details(self, telegram_id: str) -> dict:
        """Send a GET request to get the users details."""
        try:
            response = requests.get(f"{self.base_url}/user/telegram/{telegram_id}")
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
            }

    async def get_past_questions(self, name: str) -> dict:
        """Send a GET request to get the past questions."""
        try:
            response = requests.get(
                f"{self.base_url}/past_question/filter_by/course_title/{name}"
            )
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
            }

    async def get_past_question(self, past_question_id: str) -> dict:
        """Send a GET request to get the past question."""
        try:
            response = requests.get(f"{self.base_url}/past_question/{past_question_id}")
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
            }

    async def create_download(self, telegram_id: str, past_question_id: str) -> dict:
        """Send a POST request to create a new download."""
        try:
            response = requests.post(
                f"{self.base_url}/download",
                json={"user_telegram_id": telegram_id, "past_question_id": past_question_id},
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
            }
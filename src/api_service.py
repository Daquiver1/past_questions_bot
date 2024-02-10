"""Api module for the project."""

import requests

from model import SubscriptionTier


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

    async def create_payment_link(self, json: dict) -> dict:
        """Send a POST request to create a payment link."""
        try:
            response = requests.post(
                f"{self.base_url}/paystack/create_payment", json=json
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

    async def create_subscription_link(
        self, telegram_id: str, telegram_username: str, tier: SubscriptionTier
    ) -> dict:
        """Send a POST request to create a subscription link."""
        json = {
            "telegram_id": telegram_id,
            "telegram_username": telegram_username,
            "tier": tier.tier_name,
        }
        try:
            response = requests.post(
                f"{self.base_url}/paystack/create_subscription", json=json
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

    async def create_subscription(
        self, user_telegram_id: int, tier_name: str, amount: int, reference: str
    ) -> dict:
        """Send a POST request to create a subscription."""
        json = {
            "user_telegram_id": user_telegram_id,
            "tier": tier_name,
            "balance": int(amount),
            "transaction_id": reference,
        }
        print(json)
        try:
            response = requests.post(f"{self.base_url}/subscription", json=json)
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

    async def get_user_subscription(self, user_telegram_id: int) -> dict:
        """Send a GET request to get the subscription."""
        try:
            response = requests.get(f"{self.base_url}/subscription/{user_telegram_id}")
            response.raise_for_status()
            data = response.json()
            print(data)
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

    async def get_active_subscriptions(self) -> dict:
        """Send a GET request to get the active subscriptions."""
        try:
            response = requests.get(f"{self.base_url}/subscription/active")
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

    async def get_all_subscriptions(self) -> dict:
        """Send a GET request to get all subscriptions."""
        try:
            response = requests.get(f"{self.base_url}/subscription")
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

    async def update_subscription_balance(
        self, user_telegram_id: int, balance: int
    ) -> dict:
        """Send a PUT request to update the subscription balance."""
        json = {"user_telegram_id": user_telegram_id, "balance": balance}
        print(json)
        print(type(user_telegram_id))
        print(type(balance))
        try:
            response = requests.patch(
                f"{self.base_url}/subscription/{user_telegram_id}/{balance}",
                json=json,
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

    async def verify_payment(self, reference: str) -> dict:
        """Send a GET request to verify a payment."""
        try:
            print(reference)
            response = requests.get(
                f"{self.base_url}/paystack/verify_transaction/{reference}"
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
                json={
                    "user_telegram_id": telegram_id,
                    "past_question_id": past_question_id,
                },
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

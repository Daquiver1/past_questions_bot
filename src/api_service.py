"""Api module for the project."""

import requests

from model import SubscriptionTier


class BackendClient:
    """Client for the backend API."""

    def __init__(self, base_url: str) -> None:
        """Initialize the client."""
        self.base_url = base_url

    async def register_new_user(
        self, telegram_id: str, username: str, first_name: str, last_name: str
    ) -> dict:
        """Send a POST request to the specified endpoint."""
        json = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
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
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def get_user_details(self, telegram_id: str) -> dict:
        """Send a GET request to get the users details."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            response = requests.get(f"{self.base_url}/user/telegram", headers=headers)
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def create_payment_link(
        self, telegram_id: int, telegram_username: str, amount: int
    ) -> dict:
        """Send a POST request to create a payment link."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        json = {
            "telegram_id": telegram_id,
            "telegram_username": telegram_username,
            "amount": amount,
        }

        try:
            response = requests.post(
                f"{self.base_url}/paystack/create_payment", json=json, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def create_subscription_link(
        self, telegram_id: str, telegram_username: str, tier: SubscriptionTier
    ) -> dict:
        headers = {"X-Telegram-ID": str(telegram_id)}
        """Send a POST request to create a subscription link."""
        json = {
            "telegram_id": telegram_id,
            "telegram_username": telegram_username,
            "tier": tier.tier_name,
        }
        try:
            response = requests.post(
                f"{self.base_url}/paystack/create_subscription",
                json=json,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def create_subscription(
        self, telegram_id: int, tier_name: str, amount: int, reference: str
    ) -> dict:
        """Send a POST request to create a subscription."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        json = {
            "user_telegram_id": telegram_id,
            "tier": tier_name,
            "balance": int(amount),
            "transaction_id": reference,
        }
        try:
            response = requests.post(
                f"{self.base_url}/subscription", json=json, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def get_user_subscription(self, telegram_id: int) -> dict:
        """Send a GET request to get the subscription."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            response = requests.get(
                f"{self.base_url}/subscription/telegram", headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def get_active_subscriptions(self, telegram_id: int) -> dict:
        """Send a GET request to get the active subscriptions."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            response = requests.get(
                f"{self.base_url}/subscription/active", headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def get_all_subscriptions(self, telegram_id: int) -> dict:
        """Send a GET request to get all subscriptions."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            response = requests.get(f"{self.base_url}/subscription", headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def update_subscription_balance(self, telegram_id: int, balance: int) -> dict:
        """Send a PUT request to update the subscription balance."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        json = {"user_telegram_id": telegram_id, "balance": balance}
        try:
            response = requests.patch(
                f"{self.base_url}/subscription/{balance}", json=json, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def verify_payment(self, telegram_id: int, reference: str) -> dict:
        """Send a GET request to verify a payment."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            response = requests.get(
                f"{self.base_url}/paystack/verify_transaction/{reference}",
                headers=headers,
            )
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def get_past_questions(self, telegram_id: int, name: str) -> dict:
        """Send a GET request to get the past questions."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            response = requests.get(
                f"{self.base_url}/past_question/filter_by/course_title/{name}",
                headers=headers,
            )
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def get_past_question(self, telegram_id: int, past_question_id: str) -> dict:
        """Send a GET request to get the past question."""
        try:
            headers = {"X-Telegram-ID": str(telegram_id)}
            response = requests.get(
                f"{self.base_url}/past_question/{past_question_id}", headers=headers
            )
            response.raise_for_status()

            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

    async def create_download(self, telegram_id: str, past_question_id: str) -> dict:
        """Send a POST request to create a new download."""
        headers = {"X-Telegram-ID": str(telegram_id)}
        json = {
            "user_telegram_id": telegram_id,
            "past_question_id": past_question_id,
        }

        try:
            response = requests.post(
                f"{self.base_url}/download", json=json, headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "data": data}
        except requests.HTTPError as http_err:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Other error occurred: {e}",
                "status_code": None,
            }

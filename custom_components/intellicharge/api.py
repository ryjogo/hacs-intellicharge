"""API client for IntelliCharge."""
import logging
from datetime import datetime, timedelta

import aiohttp

_LOGGER = logging.getLogger(__name__)

API_BASE_URL = "https://api.intellicharge.ai"
API_LOGIN_URL = f"{API_BASE_URL}/api/v1/login/access-token"
API_SAVING_URL = f"{API_BASE_URL}/api/v2/product/pvms-ems/saving/period"
API_CUSTOM_CHARGING_RULE_URL = f"{API_BASE_URL}/api/v1/custom-charging-rule"


class IntelliChargeAPI:
    """API client for IntelliCharge."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
        inverter_id: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._username = username
        self._password = password
        self._inverter_id = inverter_id
        self._access_token = None

    async def _get_access_token(self) -> str:
        """Get or refresh access token."""
        data = {
            "username": self._username,
            "password": self._password,
        }

        async with self._session.post(API_LOGIN_URL, data=data) as response:
            response.raise_for_status()
            result = await response.json()
            self._access_token = result["access_token"]
            return self._access_token

    async def async_get_data(self) -> dict:
        """Fetch data from IntelliCharge API."""
        # Get or refresh token
        if not self._access_token:
            await self._get_access_token()

        # Calculate date range (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        params = {
            "inverter_id": self._inverter_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        headers = {
            "Authorization": f"Bearer {self._access_token}",
        }

        try:
            async with self._session.get(
                API_SAVING_URL, params=params, headers=headers
            ) as response:
                if response.status == 401:
                    # Token expired, refresh and retry
                    await self._get_access_token()
                    headers["Authorization"] = f"Bearer {self._access_token}"
                    async with self._session.get(
                        API_SAVING_URL, params=params, headers=headers
                    ) as retry_response:
                        retry_response.raise_for_status()
                        return await retry_response.json()

                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching data from IntelliCharge: %s", err)
            raise

    async def async_get_custom_charging_rules(self) -> list:
        """Get custom charging rules."""
        if not self._access_token:
            await self._get_access_token()

        headers = {
            "Authorization": f"Bearer {self._access_token}",
        }

        url = f"{API_CUSTOM_CHARGING_RULE_URL}/{self._inverter_id}"

        try:
            async with self._session.get(url, headers=headers) as response:
                if response.status == 401:
                    # Token expired, refresh and retry
                    await self._get_access_token()
                    headers["Authorization"] = f"Bearer {self._access_token}"
                    async with self._session.get(url, headers=headers) as retry_response:
                        retry_response.raise_for_status()
                        return await retry_response.json()

                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching custom charging rules: %s", err)
            raise

    async def async_set_custom_charging_rules(self, rules: list) -> bool:
        """Set custom charging rules.

        Args:
            rules: List of rule dictionaries with the following structure:
                {
                    "monday": bool,
                    "tuesday": bool,
                    "wednesday": bool,
                    "thursday": bool,
                    "friday": bool,
                    "saturday": bool,
                    "sunday": bool,
                    "valid_from": "HH:MM:SS",
                    "valid_to": "HH:MM:SS",
                    "max_charge": int,
                    "max_discharge": int or None,
                    "max_battery_soc": int or None,
                    "min_battery_soc": int or None,
                    "min_battery_soc_for_sell": int or None
                }
        """
        if not self._access_token:
            await self._get_access_token()

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        url = f"{API_CUSTOM_CHARGING_RULE_URL}/{self._inverter_id}"

        try:
            async with self._session.post(url, json=rules, headers=headers) as response:
                if response.status == 401:
                    # Token expired, refresh and retry
                    await self._get_access_token()
                    headers["Authorization"] = f"Bearer {self._access_token}"
                    async with self._session.post(url, json=rules, headers=headers) as retry_response:
                        retry_response.raise_for_status()
                        return True

                response.raise_for_status()
                return True

        except aiohttp.ClientError as err:
            _LOGGER.error("Error setting custom charging rules: %s", err)
            raise

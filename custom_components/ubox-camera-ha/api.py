"""API client for Ubox portal."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List
from datetime import datetime, timezone

import hmac
import hashlib
import base64
from typing import Union

import aiohttp
from aiohttp import ClientSession, ClientTimeout

from .const import API_BASE_URL, API_DEVICE_LIST_ENDPOINT

_LOGGER = logging.getLogger(__name__)


def hmacSha1Base64(data: Union[str, bytes]) -> str:
    # Ensure we work with bytes internally
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data

    # --- HMAC‑SHA‑1 with an empty key ---------------------------------
    # Empty key is represented by b'' (zero‑length byte string)
    hmac_obj = hmac.new(key=b"", msg=data_bytes, digestmod=hashlib.sha1)
    digest_bytes = hmac_obj.digest()  # raw binary digest (20 bytes)

    # --- Base‑64 encode ------------------------------------------------
    b64_encoded = base64.b64encode(digest_bytes).decode("ascii")

    # --- Replace the last character with a comma -----------------------
    # Equivalent to JavaScript's .replace(/.$/, ',')
    if b64_encoded:
        modified_signature = b64_encoded[:-1] + ","
    else:
        # Edge case – empty string (should never happen for a real digest)
        modified_signature = ","

    return modified_signature


class UboxApiError(Exception):
    """Exception to indicate a general API error."""


class UboxAuthError(UboxApiError):
    """Exception to indicate an authentication error."""


class UboxApiClient:
    """API client for Ubox portal."""

    def __init__(self, session: ClientSession, username: str, password: str) -> None:
        """Initialize the API client."""
        self._session = session
        self._username = username
        self._password = password
        self._auth_token = None
        self._base_url = API_BASE_URL
        self._timeout = ClientTimeout(total=30)

    async def authenticate(self) -> bool:
        """Authenticate with the Ubox API."""
        try:
            # Note: This is a placeholder for authentication
            # You may need to adjust this based on the actual Ubox API authentication method
            auth_data = {
                "account": self._username,
                "password": hmacSha1Base64(self._password),
                "lang": "en",
                "app": "ubox",
                "device_token": "dgffr486dgfr0egrferfrgg4778l5e",
                "app_version": "1.1.115",
                "brand": "iPhone15,2(18.1)",
                "device_type": 2,
            }

            headers = {
                "method": "POST",
                "scheme": "https",
                "path": "/api/v3/login",
                "authority": "portal.ubianet.com",
                "accept": "*/*",
                "content-type": "application/json",
            }

            async with self._session.post(
                "https://portal.ubianet.com/api/v3/login",
                json=auth_data,
                headers=headers,
                timeout=self._timeout,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self._auth_token = data.get("data").get("Token")

                    return True
                elif response.status == 401:
                    raise UboxAuthError("Invalid credentials")
                else:
                    raise UboxApiError(
                        f"Authentication failed with status {response.status}"
                    )

        except asyncio.TimeoutError as err:
            raise UboxApiError("Timeout during authentication") from err
        except aiohttp.ClientError as err:
            raise UboxApiError(
                f"Connection error during authentication: {err}"
            ) from err

    async def get_device_list(self) -> List[Dict[str, Any]]:
        """Get the list of devices from the API."""
        if not self._auth_token:
            await self.authenticate()

        try:
            headers = {
                "method": "POST",
                "scheme": "https",
                "path": API_DEVICE_LIST_ENDPOINT,
                "authority": "portal.ubianet.com",
                "accept": "*/*",
                "content-type": "application/json",
                "x-ubia-auth-usertoken": self._auth_token,
            }

            # The API endpoint is POST, so we need to send a POST request
            # You may need to adjust the payload based on the actual API requirements
            payload = {}

            async with self._session.post(
                f"{self._base_url}{API_DEVICE_LIST_ENDPOINT}",
                json=payload,
                headers=headers,
                timeout=self._timeout,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") > 0:
                        # Token might be expired, try to re-authenticate
                        self._auth_token = None
                        await self.authenticate()
                        return await self.get_device_list()

                    return self._process_device_data(data)
                elif response.status == 401:
                    # Token might be expired, try to re-authenticate
                    self._auth_token = None
                    await self.authenticate()
                    return await self.get_device_list()
                else:
                    raise UboxApiError(
                        f"API request failed with status {response.status}"
                    )

        except asyncio.TimeoutError as err:
            raise UboxApiError("Timeout during device list request") from err
        except aiohttp.ClientError as err:
            raise UboxApiError(
                f"Connection error during device list request: {err}"
            ) from err

    def _process_device_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process raw device data from the API."""
        devices = []

        # Assuming the API returns a list of devices
        # You may need to adjust this based on the actual API response structure
        device_list = raw_data.get("data", []).get("infos", [])

        for device in device_list:
            infos = device.get("dynamic_info")
            processed_device = {
                "device_uid": infos.get("device_uid"),
                "online_state": infos.get("online_state") == "2",
                "battery": infos.get("battery"),
                "is_battery_charging": infos.get("is_battery_charging"),
                "signal": int(infos.get("signal")) * 20,
                "latest_active_utc": infos.get("latest_active_utc"),
                "name": device.get("device_name", "Unknown"),
            }

            # Convert timestamp if needed
            if processed_device["latest_active_utc"]:
                try:
                    processed_device["latest_active_utc"] = datetime.fromtimestamp(
                        processed_device["latest_active_utc"], tz=timezone.utc
                    )
                except (ValueError, AttributeError):
                    _LOGGER.warning(
                        "Could not parse timestamp: %s",
                        processed_device["latest_active_utc"],
                    )
                    processed_device["latest_active_utc"] = None

            devices.append(processed_device)

        return devices

    async def close(self) -> None:
        """Close the API client session."""
        if self._session and not self._session.closed:
            await self._session.close()

"""API client for Ubia portal."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List
from datetime import datetime

import aiohttp
from aiohttp import ClientSession, ClientTimeout

from .const import API_BASE_URL, API_DEVICE_LIST_ENDPOINT

_LOGGER = logging.getLogger(__name__)


class UbiaApiError(Exception):
    """Exception to indicate a general API error."""


class UbiaAuthError(UbiaApiError):
    """Exception to indicate an authentication error."""


class UbiaApiClient:
    """API client for Ubia portal."""

    def __init__(self, session: ClientSession, username: str, password: str) -> None:
        """Initialize the API client."""
        self._session = session
        self._username = username
        self._password = password
        self._auth_token = None
        self._base_url = API_BASE_URL
        self._timeout = ClientTimeout(total=30)

    async def authenticate(self) -> bool:
        """Authenticate with the Ubia API."""
        try:
            # Note: This is a placeholder for authentication
            # You may need to adjust this based on the actual Ubia API authentication method
            auth_data = {
                "username": self._username,
                "password": self._password,
            }
            
            async with self._session.post(
                f"{self._base_url}/auth/login",
                json=auth_data,
                timeout=self._timeout,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self._auth_token = data.get("token")
                    return True
                elif response.status == 401:
                    raise UbiaAuthError("Invalid credentials")
                else:
                    raise UbiaApiError(f"Authentication failed with status {response.status}")
                    
        except asyncio.TimeoutError as err:
            raise UbiaApiError("Timeout during authentication") from err
        except aiohttp.ClientError as err:
            raise UbiaApiError(f"Connection error during authentication: {err}") from err

    async def get_device_list(self) -> List[Dict[str, Any]]:
        """Get the list of devices from the API."""
        if not self._auth_token:
            await self.authenticate()

        try:
            headers = {
                "Authorization": f"Bearer {self._auth_token}",
                "Content-Type": "application/json",
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
                    return self._process_device_data(data)
                elif response.status == 401:
                    # Token might be expired, try to re-authenticate
                    self._auth_token = None
                    await self.authenticate()
                    return await self.get_device_list()
                else:
                    raise UbiaApiError(f"API request failed with status {response.status}")
                    
        except asyncio.TimeoutError as err:
            raise UbiaApiError("Timeout during device list request") from err
        except aiohttp.ClientError as err:
            raise UbiaApiError(f"Connection error during device list request: {err}") from err

    def _process_device_data(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process raw device data from the API."""
        devices = []
        
        # Assuming the API returns a list of devices
        # You may need to adjust this based on the actual API response structure
        device_list = raw_data.get("devices", [])
        
        for device in device_list:
            processed_device = {
                "device_uid": device.get("device_uid"),
                "online_state": device.get("online_state"),
                "battery": device.get("battery"),
                "is_battery_charging": device.get("is_battery_charging"),
                "signal": device.get("signal"),
                "latest_active_utc": device.get("latest_active_utc"),
                "name": device.get("name", f"Camera {device.get('device_uid', 'Unknown')}"),
            }
            
            # Convert timestamp if needed
            if processed_device["latest_active_utc"]:
                try:
                    # Assuming the timestamp is in ISO format
                    processed_device["latest_active_utc"] = datetime.fromisoformat(
                        processed_device["latest_active_utc"].replace("Z", "+00:00")
                    )
                except (ValueError, AttributeError):
                    _LOGGER.warning(
                        "Could not parse timestamp: %s", 
                        processed_device["latest_active_utc"]
                    )
                    processed_device["latest_active_utc"] = None
            
            devices.append(processed_device)
            
        return devices

    async def close(self) -> None:
        """Close the API client session."""
        if self._session and not self._session.closed:
            await self._session.close()

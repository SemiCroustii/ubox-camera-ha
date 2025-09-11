"""Sensor platform for Ubia Cameras integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, MANUFACTURER, MODEL, SENSOR_TYPES
from . import UbiaDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ubia camera sensors based on a config entry."""
    coordinator: UbiaDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    
    if coordinator.data:
        for device in coordinator.data:
            device_uid = device.get("device_uid")
            if not device_uid:
                continue
                
            # Create a sensor for each sensor type
            for sensor_type in SENSOR_TYPES:
                entities.append(
                    UbiaCameraSensor(
                        coordinator,
                        device_uid,
                        sensor_type,
                        device.get("name", f"Camera {device_uid}"),
                    )
                )

    async_add_entities(entities)


class UbiaCameraSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Ubia camera sensor."""

    def __init__(
        self,
        coordinator: UbiaDataUpdateCoordinator,
        device_uid: str,
        sensor_type: str,
        device_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_uid = device_uid
        self._sensor_type = sensor_type
        self._device_name = device_name
        self._attr_name = f"{device_name} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{device_uid}_{sensor_type}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        
        # Set device class if available
        if SENSOR_TYPES[sensor_type]["device_class"]:
            if sensor_type == "battery":
                self._attr_device_class = SensorDeviceClass.BATTERY
            elif sensor_type == "signal":
                self._attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
            elif sensor_type == "latest_active_utc":
                self._attr_device_class = SensorDeviceClass.TIMESTAMP
        
        # Set unit of measurement
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit_of_measurement"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_uid)},
            name=self._device_name,
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="1.0",
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        # Find the device in the coordinator data
        device_data = None
        for device in self.coordinator.data:
            if device.get("device_uid") == self._device_uid:
                device_data = device
                break

        if not device_data:
            return None

        value = device_data.get(self._sensor_type)
        
        # Handle special cases for different sensor types
        if self._sensor_type == "online_state":
            # Convert boolean or string to human-readable format
            if isinstance(value, bool):
                return "Online" if value else "Offline"
            elif isinstance(value, str):
                return value.title()
            return "Unknown"
            
        elif self._sensor_type == "is_battery_charging":
            # Convert boolean to human-readable format
            if isinstance(value, bool):
                return "Charging" if value else "Not Charging"
            return "Unknown"
            
        elif self._sensor_type == "latest_active_utc":
            # Return datetime object for timestamp sensor
            if isinstance(value, datetime):
                return value
            elif isinstance(value, str):
                try:
                    return datetime.fromisoformat(value.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    _LOGGER.warning("Could not parse timestamp: %s", value)
                    return None
            return None
            
        elif self._sensor_type == "battery":
            # Ensure battery is a number between 0-100
            if isinstance(value, (int, float)):
                return max(0, min(100, value))
            return None
            
        elif self._sensor_type == "signal":
            # Signal strength should be a number (typically negative dBm)
            if isinstance(value, (int, float)):
                return value
            return None

        return value

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.native_value is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}

        # Find the device in the coordinator data
        device_data = None
        for device in self.coordinator.data:
            if device.get("device_uid") == self._device_uid:
                device_data = device
                break

        if not device_data:
            return {}

        return {
            "device_uid": self._device_uid,
            "last_updated": self.coordinator.last_update_success_time,
        }

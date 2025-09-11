"""Constants for the Ubia Cameras integration."""

DOMAIN = "ubox-camera-ha"
MANUFACTURER = "Ubia"
MODEL = "Camera"

# API Configuration
API_BASE_URL = "https://portal.ubianet.com/api/v2"
API_DEVICE_LIST_ENDPOINT = "/user/device_list"

# Sensor types
SENSOR_TYPES = {
    "online_state": {
        "name": "Online State",
        "icon": "mdi:wifi",
        "device_class": None,
        "unit_of_measurement": None,
    },
    "battery": {
        "name": "Battery",
        "icon": "mdi:battery",
        "device_class": "battery",
        "unit_of_measurement": "%",
    },
    "is_battery_charging": {
        "name": "Battery Charging",
        "icon": "mdi:battery-charging",
        "device_class": None,
        "unit_of_measurement": None,
    },
    "signal": {
        "name": "Signal Strength",
        "icon": "mdi:signal",
        "device_class": "signal_strength",
        "unit_of_measurement": "dBm",
    },
    "latest_active_utc": {
        "name": "Last Active",
        "icon": "mdi:clock-outline",
        "device_class": "timestamp",
        "unit_of_measurement": None,
    },
}

# Installation Guide for Ubia Cameras Home Assistant Integration

## Prerequisites

- Home Assistant Core 2023.1 or later
- Valid Ubia portal account with camera access
- Internet connection for API access

## Installation Steps

### 1. Download the Integration

Copy the entire `custom_components/ubia_cameras/` folder to your Home Assistant configuration directory:

```
<config>/custom_components/ubia_cameras/
```

Your directory structure should look like:
```
config/
├── custom_components/
│   └── ubia_cameras/
│       ├── __init__.py
│       ├── api.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── sensor.py
│       └── strings.json
└── configuration.yaml
```

### 2. Restart Home Assistant

Restart Home Assistant to load the new integration.

### 3. Add the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "Ubia Cameras"
4. Click on the integration when it appears
5. Enter your credentials:
   - **Username**: Your Ubia portal username
   - **Password**: Your Ubia portal password
6. Click **Submit**

### 4. Verify Installation

After successful setup, you should see:
- A new device for each camera in **Settings** → **Devices & Services** → **Ubia Cameras**
- Multiple sensors for each camera showing:
  - Online State
  - Battery Level
  - Battery Charging Status
  - Signal Strength
  - Last Active Time

## Configuration Options

The integration automatically discovers all cameras associated with your Ubia account. No additional configuration is required.

### Update Frequency

The integration updates sensor data every 5 minutes. This can be adjusted by modifying the `update_interval` in the coordinator if needed.

## Troubleshooting

### Integration Not Found

If "Ubia Cameras" doesn't appear in the integration list:
1. Verify the files are in the correct location
2. Restart Home Assistant
3. Clear your browser cache
4. Check the Home Assistant logs for errors

### Authentication Issues

If you get authentication errors:
1. Verify your Ubia portal credentials
2. Try logging into the Ubia portal website directly
3. Check if your account has camera access permissions

### No Sensors Created

If the integration loads but no sensors appear:
1. Check that your cameras are visible in the Ubia portal
2. Enable debug logging (see README.md)
3. Check the logs for API response details

### API Errors

If you encounter API connection issues:
1. Verify internet connectivity
2. Check if the Ubia portal is accessible
3. Review the API endpoint configuration in `const.py`

## Uninstallation

To remove the integration:
1. Go to **Settings** → **Devices & Services**
2. Find "Ubia Cameras" in the list
3. Click the three dots menu → **Delete**
4. Optionally, remove the `custom_components/ubia_cameras/` folder

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the Home Assistant logs
3. Create an issue on the project repository

## API Notes

This integration uses the following Ubia API:
- **Endpoint**: `https://portal.ubianet.com/api/v2/user/device_list`
- **Method**: POST
- **Authentication**: Username/Password (converted to Bearer token)

The API response is expected to contain device information including:
- `device_uid`: Unique device identifier
- `online_state`: Connection status
- `battery`: Battery level (0-100)
- `is_battery_charging`: Charging status (boolean)
- `signal`: Signal strength (dBm)
- `latest_active_utc`: Last activity timestamp

If the API response format differs from expectations, the integration may need updates to handle the actual response structure.

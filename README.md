# Ubia Cameras Home Assistant Integration

A custom Home Assistant integration for monitoring Ubia cameras through the Ubia portal API. This integration provides sensor entities for camera status, battery level, charging state, signal strength, and last activity timestamp.

## Features

- **Camera Status Monitoring**: Track online/offline state of your cameras
- **Battery Monitoring**: Monitor battery level and charging status
- **Signal Strength**: View signal strength of your cameras
- **Activity Tracking**: See when each camera was last active
- **Automatic Updates**: Data refreshes every 5 minutes
- **Device Integration**: Cameras appear as devices in Home Assistant with multiple sensors

## Sensors

For each camera, the following sensors are created:

| Sensor | Description | Unit | Device Class |
|--------|-------------|------|--------------|
| Online State | Camera connection status | - | - |
| Battery | Battery level | % | Battery |
| Battery Charging | Charging status | - | - |
| Signal Strength | Signal strength | dBm | Signal Strength |
| Last Active | Last activity timestamp | - | Timestamp |

## Installation

### Method 1: Manual Installation

1. Copy the `custom_components/ubia_cameras` folder to your Home Assistant `custom_components` directory:
   ```
   <config_directory>/custom_components/ubia_cameras/
   ```

2. Restart Home Assistant

3. Go to **Configuration** → **Integrations** → **Add Integration**

4. Search for "Ubia Cameras" and select it

5. Enter your Ubia portal credentials:
   - **Username**: Your Ubia portal username
   - **Password**: Your Ubia portal password

### Method 2: HACS (Home Assistant Community Store)

*Note: This integration is not yet available in HACS. Use manual installation for now.*

## Configuration

The integration is configured through the Home Assistant UI:

1. Navigate to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Ubia Cameras"
4. Enter your Ubia portal credentials
5. The integration will automatically discover your cameras

## API Requirements

This integration uses the Ubia portal API endpoint:
- **Endpoint**: `https://portal.ubianet.com/api/v2/user/device_list`
- **Method**: POST
- **Authentication**: Required (username/password)

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your Ubia portal username and password
   - Ensure your account has access to the camera devices

2. **No Devices Found**
   - Check that your cameras are properly registered in the Ubia portal
   - Verify the API response format matches expectations

3. **Connection Errors**
   - Check your internet connection
   - Verify the Ubia portal is accessible
   - Check Home Assistant logs for detailed error messages

### Logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.ubia_cameras: debug
```

## Development

### Project Structure

```
custom_components/ubia_cameras/
├── __init__.py          # Integration setup and coordinator
├── api.py              # API client for Ubia portal
├── config_flow.py      # Configuration flow
├── const.py            # Constants and configuration
├── manifest.json       # Integration manifest
├── sensor.py           # Sensor platform
└── strings.json        # UI translations
```

### API Client

The `UbiaApiClient` class handles:
- Authentication with the Ubia portal
- Device list retrieval
- Data processing and formatting
- Error handling and retries

### Data Coordinator

The integration uses Home Assistant's `DataUpdateCoordinator` for:
- Periodic data updates (every 5 minutes)
- Efficient data sharing between sensors
- Error handling and recovery

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is an unofficial integration and is not affiliated with Ubia. Use at your own risk.

## Support

For issues and feature requests, please use the GitHub issue tracker.

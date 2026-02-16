# Copernicus Pollen for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Home Assistant custom integration that provides pollen forecast data from **Copernicus CAMS** (Copernicus Atmosphere Monitoring Service) via the Open-Meteo API.

## Features

- 🌸 **Multiple pollen types**: Alder, Birch, Grass, Mugwort, Olive, Ragweed
- 🌍 **Works anywhere in Europe** with Copernicus CAMS coverage
- 🎛️ **Easy UI configuration** - no YAML editing needed
- 🏠 **Multiple locations** - configure different cities simultaneously
- 📊 **3-day forecast** included in sensor attributes
- 🔄 **Auto-updates** every hour
- 🆓 **100% Free** - no API keys or subscriptions required
- 📢 **Alexa compatible** - use with Alexa Media Player for announcements

## Data Source

This integration uses the **Open-Meteo Air Quality API**, which provides pollen data from the European Copernicus CAMS forecasting models. Data is provided in grains per cubic meter (grains/m³).

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/JudgePredator/ha-copernicus-pollen`
6. Select category: "Integration"
7. Click "Add"
8. Click "Install" on the Copernicus Pollen card
9. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/copernicus_pollen` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Copernicus Pollen"**
4. Enter your location details:
   - **Location Name**: Display name (e.g., "Chania")
   - **Latitude**: Your city's latitude (e.g., 35.5138)
   - **Longitude**: Your city's longitude (e.g., 24.0180)
5. Click **Submit**

### Finding Your Coordinates

- Google Maps: Right-click on your location → Click coordinates to copy
- Or use: [https://www.latlong.net/](https://www.latlong.net/)

## Sensors Created

After configuration, the following sensors will be created:

- `sensor.copernicus_pollen_[location]_alder`
- `sensor.copernicus_pollen_[location]_birch`
- `sensor.copernicus_pollen_[location]_grass`
- `sensor.copernicus_pollen_[location]_mugwort`
- `sensor.copernicus_pollen_[location]_olive`
- `sensor.copernicus_pollen_[location]_ragweed`

Each sensor includes:
- **State**: Current pollen level (grains/m³)
- **Attributes**: 3-day forecast, last update time, coordinates

## Pollen Level Interpretation

General guidelines (varies by pollen type and individual sensitivity):

| Level | Grains/m³ | Description |
|-------|-----------|-------------|
| Very Low | 0-10 | Minimal impact |
| Low | 10-30 | Slight symptoms possible |
| Moderate | 30-100 | Noticeable symptoms |
| High | 100-500 | Strong symptoms |
| Very High | 500+ | Severe symptoms |

## Examples

### Dashboard Card

See [examples/dashboard_card.yaml](examples/dashboard_card.yaml) for a complete Lovelace card example.

### Alexa Announcements

See [examples/alexa_automation.yaml](examples/alexa_automation.yaml) for Alexa Media Player automation examples.

**Requirements for Alexa:**
1. Install [Alexa Media Player](https://github.com/alandtse/alexa_media_player) from HACS (100% free)
2. Use the provided automation templates

## Use Cases

- 📱 Get morning pollen notifications before outdoor activities
- 🪟 Automate window closing when pollen levels are high
- 💊 Set medication reminders based on pollen forecasts
- 📊 Track pollen trends over time
- 🏃 Plan outdoor exercise when pollen is low

## Supported Regions

This integration works anywhere covered by Copernicus CAMS European air quality forecasts, including:
- 🇬🇷 Greece (all regions including Crete, Athens, Thessaloniki)
- 🇪🇸 Spain
- 🇮🇹 Italy  
- 🇫🇷 France
- 🇩🇪 Germany
- And all other European countries

## Troubleshooting

**No data showing?**
- Check your coordinates are correct (latitude/longitude)
- Verify you're within Europe (Copernicus CAMS coverage)
- Check Home Assistant logs for errors

**Sensors not updating?**
- Data updates hourly from Open-Meteo
- Check your internet connection
- Restart the integration from Settings → Devices & Services

## Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues
- Suggest features
- Submit pull requests
- Improve documentation

## Credits

- **Data Source**: [Open-Meteo](https://open-meteo.com/) Air Quality API
- **Pollen Models**: [Copernicus CAMS](https://atmosphere.copernicus.eu/)
- **Inspired by**: Various HACS pollen integrations for other regions

## License

MIT License - see [LICENSE](LICENSE) file for details

## Disclaimer

This integration provides forecast data for informational purposes only. Pollen sensitivity varies by individual. Always consult healthcare professionals for medical advice regarding allergies.

---

**Made with ❤️ for the Home Assistant community**

If this integration helps you, consider ⭐ starring the repository!
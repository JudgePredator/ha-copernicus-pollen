# 🌸 Copernicus Pollen for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue.svg)](https://www.home-assistant.io/)

A **Home Assistant custom integration** that brings real-time pollen forecasts from **Copernicus CAMS** (Europe's leading atmospheric monitoring service) directly to your smart home. Monitor pollen levels, get alerts when it's dangerous to go outside, and automate your home based on air quality.

> **Perfect for allergy sufferers!** Track the pollen types that affect you most and get notifications before symptoms start.

> **⚡ Latest (v1.0.4):** Fixed critical bug - entities now display properly with correct last_update attribute!

---

## ✨ Features

### 🌼 Comprehensive Pollen Monitoring
- **7 Individual Sensors** - Track each pollen type separately:
  - 🌳 **Olive** (major allergen in Mediterranean)
  - 🌾 **Grass** (common spring/summer allergen)
  - 🌲 **Birch** (early spring allergen)
  - 🌲 **Alder** (winter/early spring)
  - 🌺 **Ragweed** (late summer/fall)
  - 🌿 **Mugwort** (summer allergen)
  - ⚡ **Total Pollen** (sum of all types for overall air quality)

### 🎨 Smart Visual Indicators
- **Dynamic Icons** that change based on severity:
  - 🟢 Green (Very Low/Low) - Safe to go outside
  - 🟡 Yellow (Moderate) - Caution for sensitive people
  - 🔴 Red Alert (High) - Limit outdoor activities
  - ⛔ Danger (Very High) - Stay indoors!
- Different plant icons for each pollen type
- Color-coded severity levels in entity attributes

### 📊 Detailed Forecasts
- **3-day forecast** with daily averages and peak values
- **Hourly data** for precise tracking
- **Health advice** based on current levels
- **Severity ratings**: Very Low, Low, Moderate, High, Very High

### 🏠 Easy Integration
- ✅ **UI Configuration** - No YAML editing needed
- ✅ **Multiple Locations** - Monitor different cities simultaneously
- ✅ **Auto-updates** every hour
- ✅ **Works with Alexa** - Free voice announcements via Alexa Media Player
- ✅ **HACS Compatible** - Easy installation and updates
- ✅ **100% Free** - No API keys or subscriptions required
- ✅ **Stable Entity IDs** - Re-add same location without orphaned entities (v1.0.3+)

### 🌍 European Coverage
Works anywhere covered by Copernicus CAMS forecasts:
- 🇬🇷 **Greece** (Athens, Thessaloniki, Crete, all islands)
- 🇪🇸 Spain • 🇮🇹 Italy • 🇫🇷 France • 🇩🇪 Germany
- 🇵🇹 Portugal • 🇳🇱 Netherlands • 🇧🇪 Belgium • 🇦🇹 Austria
- And all other European countries!

---

## 📸 What You'll Get

After installation, you'll see **7 sensors** for your location:

```
sensor.pollen_monitor_athens_olive          → 45.2 grains/m³ 🌳
sensor.pollen_monitor_athens_grass          → 12.8 grains/m³ 🌾
sensor.pollen_monitor_athens_birch          → 0.5 grains/m³  🌲
sensor.pollen_monitor_athens_alder          → 2.1 grains/m³  🌲
sensor.pollen_monitor_athens_ragweed        → 0.0 grains/m³  🌺
sensor.pollen_monitor_athens_mugwort        → 1.3 grains/m³  🌿
sensor.pollen_monitor_athens_total_pollen   → 62 grains/m³   ⚡
```

**Each sensor includes:**
- Current pollen level (grains/m³)
- Severity rating (Very Low → Very High)
- Health advice for current conditions
- 3-day forecast (today, tomorrow, day after)
- Last update timestamp
- Geographic coordinates

---

## 📥 Installation

### Via HACS (Recommended)

1. **Open HACS** in Home Assistant
2. Click **Integrations**
3. Click the **⋮** menu (three dots) in the top right
4. Select **Custom repositories**
5. **Add this URL:**
   ```
   https://github.com/JudgePredator/ha-copernicus-pollen
   ```
6. **Category:** Integration
7. Click **Add**
8. Find **"Copernicus Pollen"** in the list
9. Click **Download**
10. **Restart Home Assistant**

### Manual Installation

1. Download the [latest release](https://github.com/JudgePredator/ha-copernicus-pollen/releases)
2. Extract and copy the `custom_components/copernicus_pollen` folder to your Home Assistant `custom_components` directory
3. Your folder structure should look like:
   ```
   /config/custom_components/copernicus_pollen/
   ├── __init__.py
   ├── manifest.json
   ├── sensor.py
   ├── config_flow.py
   ├── const.py
   └── translations/
   ```
4. Restart Home Assistant

---

## ⚙️ Configuration

### Step-by-Step Setup

1. Go to **Settings** → **Devices & Services**
2. Click the **+ Add Integration** button
3. Search for **"Copernicus Pollen"**
4. Enter your location details:

   | Field | Example | Description |
   |-------|---------|-------------|
   | **Location Name** | Athens | Display name for your sensors |
   | **Latitude** | 37.9838 | Your city's latitude |
   | **Longitude** | 23.7275 | Your city's longitude |

5. Click **Submit**
6. **Done!** Your sensors will appear immediately

### 📍 Finding Your Coordinates

**Google Maps Method:**
1. Open [Google Maps](https://maps.google.com)
2. Right-click on your location
3. Click the coordinates to copy them
4. Example: `37.9838, 23.7275`

**Other Tools:**
- [latlong.net](https://www.latlong.net/) - Search by city name
- [gps-coordinates.net](https://gps-coordinates.net/) - Multiple formats

### 🌍 Popular Greek Locations

| City | Latitude | Longitude |
|------|----------|----------|
| **Athens** | 37.9838 | 23.7275 |
| **Thessaloniki** | 40.6401 | 22.9444 |
| **Patras** | 38.2466 | 21.7346 |
| **Heraklion (Crete)** | 35.3387 | 25.1442 |
| **Rhodes** | 36.4341 | 28.2176 |
| **Corfu** | 39.6243 | 19.9217 |

---

## 📊 Understanding Pollen Levels

### Severity Scale

| Level | Grains/m³ | Icon | Description | Health Advice |
|-------|-----------|------|-------------|---------------|
| **Very Low** | 0-10 | 🟢 | Minimal impact | No precautions needed |
| **Low** | 10-30 | 🟢 | Slight symptoms | Safe for most people |
| **Moderate** | 30-100 | 🟡 | Noticeable symptoms | Sensitive individuals be cautious |
| **High** | 100-500 | 🔴 | Strong symptoms | Limit outdoor activities |
| **Very High** | 500+ | ⛔ | Severe symptoms | Stay indoors, take medication |

> **Note:** Thresholds vary by pollen type and individual sensitivity. The Total Pollen sensor gives you overall air quality at a glance.

---

## 🎯 Usage Examples

### Quick Dashboard Card

Add to your Lovelace dashboard:

```yaml
type: entities
title: 🌸 Pollen Levels Today
entities:
  - entity: sensor.pollen_monitor_athens_total_pollen
    name: Total Pollen
    icon: mdi:flower-pollen
  - type: divider
  - entity: sensor.pollen_monitor_athens_olive
    name: Olive
  - entity: sensor.pollen_monitor_athens_grass
    name: Grass
  - entity: sensor.pollen_monitor_athens_birch
    name: Birch
```

### High Pollen Alert

Get notified when it's dangerous to go outside:

```yaml
alias: High Pollen Alert
trigger:
  - platform: numeric_state
    entity_id: sensor.pollen_monitor_athens_total_pollen
    above: 100
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "⚠️ High Pollen Alert!"
      message: "Total pollen is {{ states('sensor.pollen_monitor_athens_total_pollen') }} grains/m³. Stay indoors!"
```

### Morning Pollen Report (Alexa)

**Requirements:** Install [Alexa Media Player](https://github.com/alandtse/alexa_media_player) from HACS (100% FREE)

```yaml
alias: Morning Pollen Report
trigger:
  - platform: time
    at: "07:00:00"
action:
  - service: notify.alexa_media
    data:
      target: media_player.echo_bedroom
      data:
        type: announce
      message: >
        Good morning! Today's total pollen level is 
        {{ states('sensor.pollen_monitor_athens_total_pollen') }} grains per cubic meter.
        {% set severity = state_attr('sensor.pollen_monitor_athens_total_pollen', 'severity') %}
        Pollen is {{ severity }}.
        {% if severity in ['High', 'Very High'] %}
        Consider taking your allergy medication before going outside.
        {% endif %}
```

See [examples/alexa_automation.yaml](examples/alexa_automation.yaml) for 6+ automation templates!

---

## 🔧 Advanced Features

### Accessing Forecast Data

Each sensor has forecast attributes:

```yaml
# Check tomorrow's olive pollen forecast
{{ state_attr('sensor.pollen_monitor_athens_olive', 'forecast_tomorrow_max') }}

# Get health advice
{{ state_attr('sensor.pollen_monitor_athens_olive', 'health_advice') }}

# See pollen breakdown from total sensor
{{ state_attr('sensor.pollen_monitor_athens_total_pollen', 'pollen_breakdown') }}

# Find dominant pollen type
{{ state_attr('sensor.pollen_monitor_athens_total_pollen', 'dominant_pollen') }}
```

### Multiple Locations

Monitor multiple cities:
1. Add the integration again (Settings → Devices & Services → Add Integration)
2. Enter different coordinates
3. Give it a different name (e.g., "Thessaloniki")
4. You'll get separate sensors for each location

---

## ❓ Troubleshooting

### "Entity Unavailable" Error

**Fixed in v1.0.4!** If you upgraded from an older version and entities show unavailable:

1. **Restart Home Assistant** after HACS update
2. Wait 1-2 minutes for first data fetch
3. Check logs for any errors: Settings → System → Logs → Search "copernicus_pollen"

### "Entity No Longer Provided" Warning

**Fixed in v1.0.3!** If you see this after updating from older versions:

1. **Delete old orphaned entities:**
   - Settings → Devices & Services → Entities
   - Search: `copernicus_pollen`
   - Delete entities showing "no longer provided"

2. **Restart Home Assistant**

3. **Your current entities will remain stable** - they use coordinates-based unique IDs now

### No Sensors Appearing?

1. **Check Integration Status**
   - Go to Settings → Devices & Services
   - Find "Copernicus Pollen"
   - Make sure it shows "OK" (not "Failed setup")

2. **Verify Entity Names**
   - Go to Developer Tools → States
   - Search for `sensor.pollen_monitor`
   - Entities should appear with your location name

3. **Check Logs**
   - Go to Settings → System → Logs
   - Search for "copernicus_pollen"
   - Look for any error messages

### Detailed Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for comprehensive debugging guide.

---

## 🎓 Use Cases & Ideas

### For Allergy Sufferers
- 📱 Morning notifications with daily pollen forecast
- 💊 Medication reminders when pollen is high
- 🪟 Smart window automations (close when pollen peaks)
- 🏃 Exercise planning (outdoor activities when pollen is low)

### Smart Home Automations
- **Air Purifier Control** - Turn on when pollen is high
- **HVAC Integration** - Switch to recirculation mode
- **Smart Blinds** - Close during peak pollen hours
- **Garden Irrigation** - Avoid watering when high pollen (spreads it)

### Family Notifications
- Alert family members with allergies
- Send school reminders ("high pollen, bring medication")
- Warn before outdoor events (picnics, sports)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 **Report bugs** via [GitHub Issues](https://github.com/JudgePredator/ha-copernicus-pollen/issues)
- 💡 **Suggest features** you'd like to see
- 📝 **Improve documentation** (translations, examples)
- 🔧 **Submit pull requests** with fixes or enhancements
- ⭐ **Star the repository** to show support

---

## 📚 Data Source & Credits

### Data Provider
- **Open-Meteo Air Quality API** - [open-meteo.com](https://open-meteo.com/)
- **Copernicus CAMS** - [atmosphere.copernicus.eu](https://atmosphere.copernicus.eu/)
- European Centre for Medium-Range Weather Forecasts (ECMWF)

### Pollen Models
Data comes from the **Copernicus Atmosphere Monitoring Service (CAMS)** European air quality forecasts, which use advanced atmospheric models to predict pollen concentrations across Europe.

### License
MIT License - Free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

### Acknowledgments
- **Created by:** [JudgePredator](https://github.com/JudgePredator)
- **AI Assistant:** Perplexity AI (Claude Sonnet 4.5)
- Home Assistant community for HACS and integration standards
- Open-Meteo for providing free, no-authentication API access
- Copernicus programme for open European Earth observation data

---

## ⚠️ Disclaimer

This integration provides **forecast data for informational purposes only**. Pollen sensitivity varies greatly between individuals. 

- Always consult healthcare professionals for medical advice
- Use this data as a general guide, not medical diagnosis
- Individual reactions to pollen can vary significantly
- Forecast accuracy depends on atmospheric model performance

---

## 📞 Support

- **Issues & Bugs:** [GitHub Issues](https://github.com/JudgePredator/ha-copernicus-pollen/issues)
- **Feature Requests:** [GitHub Discussions](https://github.com/JudgePredator/ha-copernicus-pollen/discussions)
- **Home Assistant Community:** [community.home-assistant.io](https://community.home-assistant.io/)

---

## 🌟 Show Your Support

If this integration helps you manage allergies better:
- ⭐ **Star this repository** on GitHub
- 🗣️ **Share** with others who have allergies
- 💬 **Post** about it on the Home Assistant community
- ☕ **Sponsor** development (optional, link in GitHub profile)

---

## 📋 Changelog

### v1.0.4 (Latest)
- 🐛 **Critical Fix:** Corrected `last_update` attribute error
- ✅ Entities now display properly without AttributeError
- ✅ Changed `last_update_success_time` to `last_update_success`

### v1.0.3
- 🔧 **Fixed:** Stable entity unique IDs based on coordinates
- ✅ No more "orphaned entities" when re-adding integration
- ✅ Delete and re-add same location without issues

### v1.0.2
- 🐛 Fixed entity availability issues
- ✨ Added proper credits in UI
- 📚 Created comprehensive troubleshooting guide
- 📝 Improved error logging

### v1.0.1
- ✨ Added Total Pollen sensor
- 🎨 Dynamic icons based on danger levels
- 💊 Health advice in attributes
- 📊 Severity ratings

### v1.0.0
- 🎉 Initial release
- 🌸 6 pollen type sensors
- 📈 3-day forecasts
- 🌍 European coverage

---

<div align="center">

**Made with ❤️ for the Home Assistant community**

*Helping allergy sufferers breathe easier, one automation at a time* 🌸

[Report Bug](https://github.com/JudgePredator/ha-copernicus-pollen/issues) • [Request Feature](https://github.com/JudgePredator/ha-copernicus-pollen/issues) • [Home Assistant](https://www.home-assistant.io/)

</div>
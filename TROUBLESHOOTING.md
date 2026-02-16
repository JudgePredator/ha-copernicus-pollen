# 🔧 Troubleshooting Guide

## "Entity Unavailable" Error

If all your sensors show as **"This entity is unavailable"**, follow these steps:

### 🔍 Step 1: Check Home Assistant Logs

1. Go to **Settings** → **System** → **Logs**
2. Search for: `copernicus_pollen`
3. Look for error messages

**Common errors and fixes:**

#### Error: "API returned status 400"
```
Error communicating with API: 400, message='Bad Request'
```

**Fix:** API parameters issue (fixed in v1.0.2+)
- Update to latest version via HACS
- Delete and re-add the integration

#### Error: "Cannot connect" or "Timeout"
```
Error communicating with API: Cannot connect to host
```

**Fix:** Internet connection or firewall issue
- Check your Home Assistant has internet access
- Test: `ping open-meteo.com` from HA
- Check firewall isn't blocking `air-quality-api.open-meteo.com`

#### Error: "No 'hourly' data in API response"
```
Invalid data received from API - missing 'hourly' key
```

**Fix:** API response format changed or location issue
- Verify coordinates are correct (not swapped)
- Ensure you're in Europe (Copernicus CAMS coverage only)
- Update to latest integration version

---

### 🔄 Step 2: Restart Integration

1. Go to **Settings** → **Devices & Services**
2. Find **"Copernicus Pollen"**
3. Click the **⋮** menu (three dots)
4. Select **"Reload"**
5. Wait 30 seconds
6. Check if sensors now show data

---

### 🗑️ Step 3: Delete & Reinstall Integration

If reloading doesn't work:

1. **Delete the integration:**
   - Settings → Devices & Services
   - Find "Copernicus Pollen"
   - Click ⋮ → **Delete**

2. **Update files via HACS:**
   - HACS → Integrations
   - Find "Copernicus Pollen"
   - Click **"Redownload"** or **"Update"**

3. **Restart Home Assistant:**
   - Settings → System → **Restart**

4. **Re-add integration:**
   - Settings → Devices & Services → **Add Integration**
   - Search: "Copernicus Pollen"
   - Enter your coordinates:
     - **Name:** Chania (or your city)
     - **Latitude:** 35.5138 (your latitude)
     - **Longitude:** 24.0180 (your longitude)

5. **Wait 1-2 minutes** for first data fetch

---

### 🧪 Step 4: Manual Update via SSH/File Editor

If HACS update isn't working:

1. **Access your HA config folder** (via SSH or File Editor)

2. **Navigate to:**
   ```
   /config/custom_components/copernicus_pollen/
   ```

3. **Check these files exist:**
   - `__init__.py`
   - `manifest.json` (should show version 1.0.2 or higher)
   - `sensor.py`
   - `config_flow.py`
   - `const.py`
   - `strings.json`
   - `translations/en.json`

4. **Delete the entire folder:**
   ```bash
   rm -rf /config/custom_components/copernicus_pollen
   ```

5. **Re-download via HACS**

6. **Restart Home Assistant**

---

## No Sensors Appearing

### Symptoms
- Integration shows "OK" status
- But no entities created
- Device shows 0 entities

### Fix

1. **Check entity registry:**
   - Developer Tools → **States**
   - Search: `sensor.pollen_monitor`
   - Do any entities appear?

2. **Check device:**
   - Settings → Devices & Services → Copernicus Pollen
   - Click on the device
   - Should show 7 entities

3. **If entities exist but hidden:**
   - Go to device page
   - Click each entity
   - Check if "Hide" toggle is ON
   - Turn it OFF

4. **If no entities at all:**
   - Delete integration completely
   - Delete `/config/custom_components/copernicus_pollen/`
   - Reinstall from HACS
   - Restart HA
   - Add integration again

---

## Wrong Location Data

### Symptoms
- Sensors show but data seems wrong
- Pollen levels don't match local conditions

### Fix

1. **Verify coordinates:**
   - Check you didn't swap latitude/longitude
   - Latitude: -90 to 90 (Greece ~35-41)
   - Longitude: -180 to 180 (Greece ~19-28)

2. **Test coordinates:**
   - Paste in Google Maps: `35.5138, 24.0180`
   - Should point to your city

3. **Delete and reconfigure:**
   - Settings → Devices & Services
   - Delete Copernicus Pollen
   - Add again with correct coordinates

---

## Sensors Not Updating

### Symptoms
- Sensors created successfully
- But values never change
- "last_update" attribute is old

### Fix

1. **Check update interval:**
   - Integration updates every **1 hour**
   - Check `last_update` attribute
   - Should update within 60 minutes

2. **Force update:**
   - Settings → Devices & Services
   - Copernicus Pollen → ⋮ → **Reload**

3. **Check logs for errors:**
   - Look for repeated API errors
   - Fix any connection issues

4. **Verify internet:**
   - Test from HA terminal:
     ```bash
     curl "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=35.5&longitude=24&hourly=alder_pollen"
     ```
   - Should return JSON data

---

## HACS Shows Commit Hash Instead of Version

### Symptoms
- HACS shows version as `f50d71b` or similar hash
- Instead of `v1.0.2`

### Fix

Repository needs a GitHub Release:

1. Go to: https://github.com/JudgePredator/ha-copernicus-pollen/releases
2. Check if **v1.0.2** release exists
3. If not, create release:
   - Click "Create a new release"
   - Tag: `v1.0.2`
   - Title: `v1.0.2`
   - Publish

4. In HACS:
   - Find integration
   - Click **"Redownload"**
   - Should now show v1.0.2

---

## Integration Not Found in HACS

### Symptoms
- Can't find "Copernicus Pollen" in HACS search
- Even after adding custom repository

### Fix

1. **Add as custom repository:**
   - HACS → Integrations → ⋮ (menu)
   - **Custom repositories**
   - URL: `https://github.com/JudgePredator/ha-copernicus-pollen`
   - Category: **Integration**
   - Click **Add**

2. **Wait 30 seconds** for HACS to process

3. **Search again:**
   - HACS → Integrations
   - Search: "Copernicus" or "Pollen"
   - Should appear now

4. **If still not showing:**
   - Check repository URL is correct
   - Verify `hacs.json` exists in repo
   - Restart Home Assistant
   - Try adding custom repo again

---

## Alexa Not Announcing

### Symptoms
- Sensors work fine
- But Alexa doesn't announce pollen levels
- Automation doesn't trigger

### Fix

1. **Install Alexa Media Player:**
   - Must have [Alexa Media Player](https://github.com/alandtse/alexa_media_player) from HACS
   - This is separate integration
   - 100% free, no subscriptions

2. **Configure Alexa Media Player:**
   - Settings → Devices & Services
   - Find "Alexa Media Player"
   - Log in with Amazon account

3. **Find your Echo device:**
   - Developer Tools → States
   - Search: `media_player.echo`
   - Note exact entity_id (e.g., `media_player.echo_bedroom`)

4. **Test announcement:**
   - Developer Tools → Services
   - Service: `notify.alexa_media`
   - Target: your Echo device
   - Message: "Test announcement"
   - Call service

5. **Update automation:**
   - Replace `media_player.YOUR_ECHO_DEVICE`
   - With your actual entity_id

---

## Docker/Container Issues

### Symptoms
- Running HA in Docker
- Integration not showing in overview
- Entities unavailable

### Fix

1. **Check file permissions:**
   ```bash
   ls -la /config/custom_components/copernicus_pollen/
   ```
   - Should be readable by HA user

2. **Verify mount:**
   - Custom components folder must be mounted
   - Docker compose:
     ```yaml
     volumes:
       - /path/to/config:/config
     ```

3. **Restart container:**
   ```bash
   docker restart homeassistant
   ```

4. **Check logs:**
   ```bash
   docker logs homeassistant | grep copernicus_pollen
   ```

---

## Still Not Working?

### 💬 Get Help

1. **Enable debug logging:**
   
   Edit `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.copernicus_pollen: debug
   ```

2. **Restart HA** and reproduce the issue

3. **Collect information:**
   - Home Assistant version
   - Integration version (from manifest.json)
   - Full error log
   - Your coordinates (approximate)
   - Docker or HA OS?

4. **Create GitHub Issue:**
   - Go to: https://github.com/JudgePredator/ha-copernicus-pollen/issues
   - Click "New Issue"
   - Provide all information above
   - Include full error log

5. **Community Help:**
   - Post in [Home Assistant Community](https://community.home-assistant.io/)
   - Tag: `custom-integration`
   - Link to this repository

---

## ✅ Quick Checklist

Before asking for help, verify:

- [ ] Home Assistant version 2024.1.0 or newer
- [ ] Integration version 1.0.2 or newer (check manifest.json)
- [ ] HACS installed and working
- [ ] Coordinates are correct (not swapped)
- [ ] Location is in Europe
- [ ] Internet connection working from HA
- [ ] Can access `https://open-meteo.com` from HA
- [ ] Home Assistant restarted after installation
- [ ] Integration reloaded after issues
- [ ] Checked logs for specific errors
- [ ] Tried deleting and re-adding integration

---

*Created by JudgePredator with Perplexity AI assistance* 🌸
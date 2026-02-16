"""The Copernicus Pollen integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_URL, POLLEN_TYPES

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Copernicus Pollen from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    coordinator = CopernicusPollenDataUpdateCoordinator(hass, entry)
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info(
        "Copernicus Pollen integration loaded for %s (%.4f, %.4f)",
        entry.data["name"],
        entry.data["latitude"],
        entry.data["longitude"]
    )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


class CopernicusPollenDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Copernicus pollen data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.latitude = entry.data["latitude"]
        self.longitude = entry.data["longitude"]
        self.location_name = entry.data["name"]
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.data['name']}",
            update_interval=timedelta(hours=1),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        session = async_get_clientsession(self.hass)
        
        # Build API URL with all pollen types
        pollen_params = ",".join(POLLEN_TYPES.keys())
        url = f"{API_URL}?latitude={self.latitude}&longitude={self.longitude}&hourly={pollen_params}&forecast_days=3"
        
        _LOGGER.debug("Fetching pollen data from: %s", url)
        
        try:
            async with async_timeout.timeout(30):
                async with session.get(url) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        _LOGGER.error(
                            "API returned status %s: %s",
                            response.status,
                            error_text
                        )
                        raise UpdateFailed(f"API returned status {response.status}")
                    
                    data = await response.json()
                    
                    _LOGGER.debug("Received data keys: %s", list(data.keys()))
                    
                    if "hourly" not in data:
                        _LOGGER.error("No 'hourly' data in API response: %s", data)
                        raise UpdateFailed("Invalid data received from API - missing 'hourly' key")
                    
                    # Process hourly data to get current values and forecasts
                    processed_data = {}
                    hourly = data["hourly"]
                    
                    _LOGGER.debug("Hourly data keys: %s", list(hourly.keys()))
                    
                    for pollen_type in POLLEN_TYPES.keys():
                        if pollen_type in hourly:
                            values = hourly[pollen_type]
                            if values and len(values) > 0:
                                # Current value is the first non-null value
                                current = next((v for v in values if v is not None), 0.0)
                                processed_data[pollen_type] = {
                                    "current": float(current),
                                    "forecast": values[:72]  # 3 days of hourly data
                                }
                                _LOGGER.debug(
                                    "Processed %s: current=%.2f, forecast points=%d",
                                    pollen_type,
                                    current,
                                    len(values[:72])
                                )
                            else:
                                _LOGGER.warning("No values for %s", pollen_type)
                                processed_data[pollen_type] = {
                                    "current": 0.0,
                                    "forecast": []
                                }
                        else:
                            _LOGGER.warning("%s not in API response", pollen_type)
                            processed_data[pollen_type] = {
                                "current": 0.0,
                                "forecast": []
                            }
                    
                    if not processed_data:
                        raise UpdateFailed("No pollen data could be processed")
                    
                    _LOGGER.info(
                        "Successfully updated pollen data for %s with %d pollen types",
                        self.location_name,
                        len(processed_data)
                    )
                    
                    return processed_data
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error fetching pollen data: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}")
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching pollen data")
            raise UpdateFailed("Timeout communicating with API")
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching pollen data")
            raise UpdateFailed(f"Unexpected error: {err}")
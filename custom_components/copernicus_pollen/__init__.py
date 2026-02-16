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
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
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
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        session = async_get_clientsession(self.hass)
        
        # Build API URL with all pollen types
        # Note: pollen parameters don't use european_aqi_ prefix
        pollen_params = ",".join(POLLEN_TYPES.keys())
        url = f"{API_URL}?latitude={self.latitude}&longitude={self.longitude}&hourly={pollen_params}&forecast_days=3"
        
        try:
            async with async_timeout.timeout(30):
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if "hourly" not in data:
                        raise UpdateFailed("Invalid data received from API")
                    
                    # Process hourly data to get current values and forecasts
                    processed_data = {}
                    hourly = data["hourly"]
                    
                    for pollen_type in POLLEN_TYPES.keys():
                        if pollen_type in hourly and hourly[pollen_type]:
                            values = hourly[pollen_type]
                            # Current value is the first non-null value
                            current = next((v for v in values if v is not None), 0)
                            processed_data[pollen_type] = {
                                "current": current,
                                "forecast": values[:72]  # 3 days of hourly data
                            }
                    
                    return processed_data
                    
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")
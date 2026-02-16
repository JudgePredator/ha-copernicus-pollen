"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, POLLEN_TYPES


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for pollen_type in POLLEN_TYPES.keys():
        entities.append(CopernicusPollenSensor(coordinator, entry, pollen_type))
    
    async_add_entities(entities)


class CopernicusPollenSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Copernicus Pollen Sensor."""

    def __init__(self, coordinator, entry, pollen_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._pollen_type = pollen_type
        self._entry = entry
        self._attr_name = f"Copernicus Pollen {entry.data['name']} {POLLEN_TYPES[pollen_type]}"
        self._attr_unique_id = f"{entry.entry_id}_{pollen_type}"
        self._attr_native_unit_of_measurement = "grains/m³"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:flower-pollen"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data and self._pollen_type in self.coordinator.data:
            return round(self.coordinator.data[self._pollen_type]["current"], 1)
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data or self._pollen_type not in self.coordinator.data:
            return {}
        
        data = self.coordinator.data[self._pollen_type]
        
        # Calculate daily averages for 3-day forecast
        forecast = data.get("forecast", [])
        daily_forecast = {}
        
        if forecast:
            for day in range(3):
                start_idx = day * 24
                end_idx = start_idx + 24
                day_values = [v for v in forecast[start_idx:end_idx] if v is not None]
                if day_values:
                    daily_forecast[f"day_{day}_avg"] = round(sum(day_values) / len(day_values), 1)
                    daily_forecast[f"day_{day}_max"] = round(max(day_values), 1)
        
        return {
            "pollen_type": POLLEN_TYPES[self._pollen_type],
            "location": self._entry.data["name"],
            "latitude": self.coordinator.latitude,
            "longitude": self.coordinator.longitude,
            "forecast_today_avg": daily_forecast.get("day_0_avg"),
            "forecast_today_max": daily_forecast.get("day_0_max"),
            "forecast_tomorrow_avg": daily_forecast.get("day_1_avg"),
            "forecast_tomorrow_max": daily_forecast.get("day_1_max"),
            "forecast_day_after_avg": daily_forecast.get("day_2_avg"),
            "forecast_day_after_max": daily_forecast.get("day_2_max"),
            "last_update": self.coordinator.last_update_success_time,
            "attribution": "Data provided by Open-Meteo (Copernicus CAMS)",
        }

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": f"Copernicus Pollen {self._entry.data['name']}",
            "manufacturer": "Copernicus CAMS",
            "model": "Pollen Forecast",
            "sw_version": "1.0.0",
            "configuration_url": "https://github.com/JudgePredator/ha-copernicus-pollen",
        }
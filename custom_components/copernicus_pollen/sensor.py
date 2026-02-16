"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN, POLLEN_TYPES

# Pollen level thresholds for icon changes
THRESHOLD_MODERATE = 30
THRESHOLD_HIGH = 100
THRESHOLD_VERY_HIGH = 500


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    
    # Add individual pollen type sensors
    for pollen_type in POLLEN_TYPES.keys():
        entities.append(CopernicusPollenSensor(coordinator, entry, pollen_type))
    
    # Add total pollen sensor
    entities.append(CopernicusPollenTotalSensor(coordinator, entry))
    
    async_add_entities(entities)


class CopernicusPollenSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Copernicus Pollen Sensor."""

    def __init__(self, coordinator, entry, pollen_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._pollen_type = pollen_type
        self._entry = entry
        self._attr_has_entity_name = True
        self._attr_name = POLLEN_TYPES[pollen_type]
        self._attr_unique_id = f"{entry.entry_id}_{pollen_type}"
        self._attr_native_unit_of_measurement = "grains/m³"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data and self._pollen_type in self.coordinator.data:
            return round(self.coordinator.data[self._pollen_type]["current"], 1)
        return None

    @property
    def icon(self):
        """Return dynamic icon based on pollen level."""
        value = self.native_value or 0
        
        # Specific icons for each pollen type with severity colors
        if self._pollen_type == "olive_pollen":
            base = "mdi:tree"
        elif self._pollen_type == "grass_pollen":
            base = "mdi:grass"
        elif self._pollen_type == "birch_pollen":
            base = "mdi:tree-outline"
        elif self._pollen_type == "alder_pollen":
            base = "mdi:pine-tree"
        elif self._pollen_type == "ragweed_pollen":
            base = "mdi:flower"
        elif self._pollen_type == "mugwort_pollen":
            base = "mdi:flower-pollen"
        else:
            base = "mdi:flower-pollen"
        
        # Add alert icon for dangerous levels
        if value >= THRESHOLD_VERY_HIGH:
            return "mdi:alert-octagon"  # Very high - danger!
        elif value >= THRESHOLD_HIGH:
            return "mdi:alert"  # High - warning
        
        return base

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
        
        # Get current level and add severity rating
        current = self.native_value or 0
        if current >= THRESHOLD_VERY_HIGH:
            severity = "Very High"
            health_advice = "Stay indoors, close windows, take allergy medication"
        elif current >= THRESHOLD_HIGH:
            severity = "High"
            health_advice = "Limit outdoor activities, consider medication"
        elif current >= THRESHOLD_MODERATE:
            severity = "Moderate"
            health_advice = "Sensitive individuals should be cautious"
        elif current >= 10:
            severity = "Low"
            health_advice = "Safe for most people"
        else:
            severity = "Very Low"
            health_advice = "No precautions needed"
        
        return {
            "pollen_type": POLLEN_TYPES[self._pollen_type],
            "severity": severity,
            "health_advice": health_advice,
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
            "name": f"Pollen Monitor {self._entry.data['name']}",
            "manufacturer": "Copernicus CAMS",
            "model": "European Air Quality Forecast",
            "sw_version": "1.0.1",
            "configuration_url": "https://github.com/JudgePredator/ha-copernicus-pollen",
        }


class CopernicusPollenTotalSensor(CoordinatorEntity, SensorEntity):
    """Representation of total pollen sensor (sum of all types)."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_has_entity_name = True
        self._attr_name = "Total Pollen"
        self._attr_unique_id = f"{entry.entry_id}_total"
        self._attr_native_unit_of_measurement = "grains/m³"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        """Return the total of all pollen types."""
        if not self.coordinator.data:
            return None
        
        total = 0
        for pollen_type in POLLEN_TYPES.keys():
            if pollen_type in self.coordinator.data:
                total += self.coordinator.data[pollen_type]["current"]
        
        return round(total, 0)

    @property
    def icon(self):
        """Return dynamic icon based on total pollen level."""
        value = self.native_value or 0
        
        if value >= THRESHOLD_VERY_HIGH:
            return "mdi:alert-octagon"  # Very high - danger!
        elif value >= THRESHOLD_HIGH:
            return "mdi:alert"  # High - warning
        elif value >= THRESHOLD_MODERATE:
            return "mdi:flower-pollen-outline"  # Moderate
        else:
            return "mdi:flower-pollen"  # Low/Normal

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        # Get current total and severity
        current = self.native_value or 0
        if current >= THRESHOLD_VERY_HIGH:
            severity = "Very High"
            health_advice = "Dangerous for allergy sufferers - stay indoors"
        elif current >= THRESHOLD_HIGH:
            severity = "High"
            health_advice = "High allergy risk - limit outdoor exposure"
        elif current >= THRESHOLD_MODERATE:
            severity = "Moderate"
            health_advice = "Moderate risk for sensitive individuals"
        elif current >= 10:
            severity = "Low"
            health_advice = "Low risk - safe for most people"
        else:
            severity = "Very Low"
            health_advice = "Very low risk - no precautions needed"
        
        # Break down by pollen type
        breakdown = {}
        for pollen_type, display_name in POLLEN_TYPES.items():
            if pollen_type in self.coordinator.data:
                value = round(self.coordinator.data[pollen_type]["current"], 1)
                breakdown[display_name.lower()] = value
        
        return {
            "severity": severity,
            "health_advice": health_advice,
            "location": self._entry.data["name"],
            "pollen_breakdown": breakdown,
            "dominant_pollen": max(breakdown, key=breakdown.get) if breakdown else None,
            "latitude": self.coordinator.latitude,
            "longitude": self.coordinator.longitude,
            "last_update": self.coordinator.last_update_success_time,
            "attribution": "Data provided by Open-Meteo (Copernicus CAMS)",
        }

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": f"Pollen Monitor {self._entry.data['name']}",
            "manufacturer": "Copernicus CAMS",
            "model": "European Air Quality Forecast",
            "sw_version": "1.0.1",
            "configuration_url": "https://github.com/JudgePredator/ha-copernicus-pollen",
        }
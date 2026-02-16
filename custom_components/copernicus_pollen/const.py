"""Constants for the Copernicus Pollen integration."""

DOMAIN = "copernicus_pollen"

# Open-Meteo Air Quality API endpoint
API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Pollen types supported by Copernicus CAMS
# Note: Use direct pollen parameter names, not european_aqi_ prefix
POLLEN_TYPES = {
    "alder_pollen": "Alder",
    "birch_pollen": "Birch",
    "grass_pollen": "Grass",
    "mugwort_pollen": "Mugwort",
    "olive_pollen": "Olive",
    "ragweed_pollen": "Ragweed",
}
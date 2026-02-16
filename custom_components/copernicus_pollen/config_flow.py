"""Config flow for Copernicus Pollen integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Defaults are intentionally set to a well-known public location (Athens)
# to avoid shipping any private/home coordinates in the repository.
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Athens"): str,
        vol.Required("latitude", default=37.9838): vol.Coerce(float),
        vol.Required("longitude", default=23.7275): vol.Coerce(float),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Copernicus Pollen."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                # Validate coordinates
                if not (-90 <= user_input["latitude"] <= 90):
                    errors["latitude"] = "invalid_latitude"
                if not (-180 <= user_input["longitude"] <= 180):
                    errors["longitude"] = "invalid_longitude"

                if not errors:
                    # Create unique ID based on coordinates
                    await self.async_set_unique_id(
                        f"{user_input['latitude']}_{user_input['longitude']}"
                    )
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=user_input["name"],
                        data=user_input,
                    )
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

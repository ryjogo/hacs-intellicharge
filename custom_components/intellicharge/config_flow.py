"""Config flow for IntelliCharge integration."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import IntelliChargeAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "intellicharge"

CONF_INVERTER_ID = "inverter_id"

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_INVERTER_ID): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for IntelliCharge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the credentials
            session = async_get_clientsession(self.hass)
            api = IntelliChargeAPI(
                session=session,
                username=user_input[CONF_USERNAME],
                password=user_input[CONF_PASSWORD],
                inverter_id=user_input[CONF_INVERTER_ID],
            )

            try:
                # Try to fetch data to validate credentials
                await api.async_get_data()
            except Exception as err:
                _LOGGER.error("Error validating credentials: %s", err)
                errors["base"] = "cannot_connect"
            else:
                # Create the config entry
                await self.async_set_unique_id(
                    f"{user_input[CONF_USERNAME]}_{user_input[CONF_INVERTER_ID]}"
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"IntelliCharge ({user_input[CONF_INVERTER_ID]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

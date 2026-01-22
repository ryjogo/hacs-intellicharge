"""IntelliCharge integration for Home Assistant."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .api import IntelliChargeAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "intellicharge"
PLATFORMS = [Platform.SENSOR]
UPDATE_INTERVAL = timedelta(minutes=15)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up IntelliCharge from a config entry."""
    session = async_get_clientsession(hass)

    api = IntelliChargeAPI(
        session=session,
        username=entry.data["username"],
        password=entry.data["password"],
        inverter_id=entry.data["inverter_id"],
    )

    coordinator = IntelliChargeDataUpdateCoordinator(hass, api)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    async def handle_set_charging_rules(call: ServiceCall) -> None:
        """Handle the set_charging_rules service call."""
        rules = call.data.get("rules")
        try:
            await api.async_set_custom_charging_rules(rules)
            await coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to set charging rules: %s", err)
            raise

    hass.services.async_register(
        DOMAIN,
        "set_charging_rules",
        handle_set_charging_rules,
        schema=vol.Schema({
            vol.Required("rules"): vol.All(cv.ensure_list, [dict])
        })
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        # Unregister services if this is the last entry
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, "set_charging_rules")

    return unload_ok


class IntelliChargeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching IntelliCharge data."""

    def __init__(self, hass: HomeAssistant, api: IntelliChargeAPI) -> None:
        """Initialize."""
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.api.async_get_data()
            # Also fetch custom charging rules
            charging_rules = await self.api.async_get_custom_charging_rules()
            return {
                "savings": data,
                "charging_rules": charging_rules,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

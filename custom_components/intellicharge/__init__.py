"""IntelliCharge integration for Home Assistant."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

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

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

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
            return await self.api.async_get_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

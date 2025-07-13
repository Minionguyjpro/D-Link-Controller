import logging
import httpx
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

GET_SCHEMA = vol.Schema({
    vol.Required("url"): cv.string,
})

SET_SCHEMA = vol.Schema({
    vol.Required("url"): cv.string,
    vol.Required("data"): dict,
})

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the D-Link Controller integration (services only)."""
    async def handle_get_details(call: ServiceCall):
        url = call.data["url"]
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            _LOGGER.info("GET %s: %s", url, resp.text)
            hass.states.async_set(f"{DOMAIN}.last_get", resp.text)
    
    async def handle_set_details(call: ServiceCall):
        url = call.data["url"]
        data = call.data["data"]
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=data)
            _LOGGER.info("POST %s: %s", url, resp.text)
            hass.states.async_set(f"{DOMAIN}.last_post", resp.text)

    hass.services.async_register(DOMAIN, "get_details", handle_get_details, schema=GET_SCHEMA)
    hass.services.async_register(DOMAIN, "set_details", handle_set_details, schema=SET_SCHEMA)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up D-Link Controller from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward entry setup to all platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
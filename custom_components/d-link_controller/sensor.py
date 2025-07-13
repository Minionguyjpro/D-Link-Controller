from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up D-Link sensors from a config entry."""
    session_token = entry.data.get("session_token")
    # TODO: Use session_token to fetch real device data
    async_add_entities([DLinkDummySensor(session_token)])

class DLinkDummySensor(SensorEntity):
    def __init__(self, session_token):
        self._attr_name = "D-Link Dummy Sensor"
        self._attr_unique_id = f"dlink_dummy_{session_token[-6:]}"
        self._attr_native_value = "online"

    @property
    def extra_state_attributes(self):
        return {"session_token": "hidden"}
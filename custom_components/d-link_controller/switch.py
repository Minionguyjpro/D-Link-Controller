import httpx
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_HOST, CONF_SESSION_TOKEN

LED_ON = "0"
LED_OFF = "1"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the D-Link LED switch from a config entry."""
    host = entry.data[CONF_HOST]
    session_token = entry.data[CONF_SESSION_TOKEN]
    async_add_entities([DLinkLEDSwitch(host, session_token)])

class DLinkLEDSwitch(SwitchEntity):
    def __init__(self, host, session_token):
        self._host = host
        self._session_token = session_token
        self._attr_name = "D-Link Camera LED"
        self._attr_is_on = None

    async def async_turn_on(self, **kwargs):
        await self._set_led(LED_ON)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self._set_led(LED_OFF)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def _set_led(self, value):
        url = f"http://{self._host}/setSystemControl"
        data = {
            "ReplySuccessPage": "advanced.htm",
            "ReplyErrorPage": "errradv.htm",
            "SessionKey": self._session_token,
            "LEDControl": value,
            "ConfigSystemControl": "Apply"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": f"http://{self._host}",
            "Connection": "keep-alive",
            "Referer": f"http://{self._host}/advanced.htm"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data, headers=headers)
            resp.raise_for_status()

    async def async_update(self):
        # Optionally implement polling to get the current LED state
        pass
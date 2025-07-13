from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_SESSION_TOKEN, CONF_HOST

class DLinkControllerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for D-Link Controller."""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"D-Link Camera ({user_input[CONF_HOST]})",
                data=user_input,
            )

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, description={"name": "Device IP Address"}): str,
            vol.Required(CONF_SESSION_TOKEN, description={"name": "Session Token"}): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
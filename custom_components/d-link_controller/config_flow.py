from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_SESSION_TOKEN, CONF_DISCOVERED_DEVICE_INFO

class DLinkControllerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for D-Link Controller."""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate session token here if needed
            return self.async_create_entry(
                title="D-Link Controller",
                data=user_input,
            )

        data_schema = vol.Schema({
            vol.Required(CONF_SESSION_TOKEN): str,
            vol.Optional(CONF_DISCOVERED_DEVICE_INFO): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
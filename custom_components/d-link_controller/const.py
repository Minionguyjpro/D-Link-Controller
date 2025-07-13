"""Constants for the d-link_controller integration."""
from datetime import timedelta
from enum import Enum
from typing import Union

from homeassistant.const import Platform

NAME = "d-link_controller"
DOMAIN = "d-link_controller"
VERSION = "1.0.0"

ISSUE_URL = "https://github.com/Minionguyjpro/D-Link-Controller/issues"

# list the platforms that you want to support.
PLATFORMS = [
    Platform.SWITCH,
    Platform.SENSOR,
#    Platform.BINARY_SENSOR,
#    Platform.LIGHT,
#    Platform.NUMBER,
#    Platform.UPDATE,
]

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_SESSION_TOKEN = "session_token"

DEFAULT_POLLING_RATE_S = 30  # 30 seconds

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
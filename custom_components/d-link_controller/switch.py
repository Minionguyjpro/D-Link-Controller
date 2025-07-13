import httpx
import hashlib
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_HOST, CONF_SESSION_TOKEN, CONF_USERNAME, CONF_PASSWORD

LED_ON = "0"
LED_OFF = "1"

def build_digest_header(username, password, method, uri, www_authenticate, body=None):
    # Parse the WWW-Authenticate header
    import re
    auth_dict = dict(re.findall(r'(\w+)="([^"]+)"', www_authenticate))
    realm = auth_dict['realm']
    nonce = auth_dict['nonce']
    qop = auth_dict.get('qop', 'auth')
    algorithm = auth_dict.get('algorithm', 'MD5')
    opaque = auth_dict.get('opaque')
    cnonce = httpx._transports.default._gen_cnonce()
    nc = "00000001"

    # Calculate HA1, HA2, and response
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode()).hexdigest()

    # Build the header
    header = (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", '
        f'uri="{uri}", response="{response}", qop={qop}, nc={nc}, cnonce="{cnonce}"'
    )
    if opaque:
        header += f', opaque="{opaque}"'
    return header

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    host = entry.data[CONF_HOST]
    session_token = entry.data[CONF_SESSION_TOKEN]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    async_add_entities([DLinkLEDSwitch(host, session_token, username, password)])

class DLinkLEDSwitch(SwitchEntity):
    def __init__(self, host, session_token, username, password):
        self._host = host
        self._session_token = session_token
        self._username = username
        self._password = password
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
        uri = "/setSystemControl"
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
            # 1. Get WWW-Authenticate header
            resp = await client.post(url, data=data, headers=headers)
            if resp.status_code == 401:
                www_auth = resp.headers.get("WWW-Authenticate")
                if not www_auth:
                    raise Exception("No WWW-Authenticate header found")
                # 2. Build Authorization header
                auth_header = build_digest_header(self._username, self._password, "POST", uri, www_auth)
                headers["Authorization"] = auth_header
                # 3. Retry with Authorization
                resp = await client.post(url, data=data, headers=headers)
            resp.raise_for_status()

    async def async_update(self):
        pass
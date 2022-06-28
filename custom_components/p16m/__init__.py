"""The Pertronic F16 Mimic integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .pertronic.PertronicMimic import PertronicMimic
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pertronic F16 Mimic from a config entry."""
    if DOMAIN not in hass.data.keys():
        _LOGGER.debug("hass.data[DOMAIN] doesn't exist, creating... ")
        hass.data[DOMAIN] = {}
    else:
        _LOGGER.debug("hass.data[DOMAIN] found")

    hass.data[DOMAIN][entry.entry_id] = PertronicMimic(
        entry.data["ip_addr"],
        entry.data["port"],
        short_name=entry.data["panel_name_short"],
    )
    hass.data[DOMAIN][entry.entry_id].start()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN][entry.entry_id].stop()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

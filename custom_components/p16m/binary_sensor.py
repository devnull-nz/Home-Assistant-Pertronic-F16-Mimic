"""Support for Binary inputs from a command centre server."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN

from .pertronic.PertronicMimic import PertronicMimic

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up entry."""

    sensors = []

    _LOGGER.info("Loading global binary sensors")
    sensors.append(P16MBinarySensor(hass.data[DOMAIN][entry.entry_id], "n", 0, entry))
    sensors.append(P16MBinarySensor(hass.data[DOMAIN][entry.entry_id], "d", 0, entry))
    sensors.append(P16MBinarySensor(hass.data[DOMAIN][entry.entry_id], "f", 0, entry))
    sensors.append(P16MBinarySensor(hass.data[DOMAIN][entry.entry_id], "s", 0, entry))

    _LOGGER.info("Loading zone binary sensors")
    for i in range(8):
        sensors.append(
            P16MBinarySensor(hass.data[DOMAIN][entry.entry_id], "z", i, entry)
        )

    async_add_entities(sensors)
    hass.data[DOMAIN][entry.entry_id].force_callbacks()


class P16MBinarySensor(BinarySensorEntity):
    """Pertronic F16 Mimic binary sensor."""

    def __init__(
        self, mimic: PertronicMimic, entity_type, entity_index, entry: ConfigEntry
    ):
        self.mimic = mimic
        self.entity_type = entity_type
        self.entity_index = entity_index

        self._is_on = None

        entity_types = {
            "n": "Normal",
            "d": "Defect",
            "f": "Fire",
            "s": "Sprinkler",
            "z": "Zone",
        }

        name_setup = ""

        if entity_type != "z":
            name_setup = entity_types[entity_type]
        else:
            name_setup = "{} {}".format(entity_types[entity_type], entity_index + 1)

        self._attr_name = "{} {}".format(mimic.get_short_name(), name_setup)
        self._attr_unique_id = "{}_{}_{}_{}".format(
            "P16M", entry.entry_id, entity_type, entity_index
        )

        if entity_type == "n":
            mimic.register_normal_callback(self.process_callback)
            self._is_on = mimic.get_normal()
        if entity_type == "d":
            mimic.register_defect_callback(self.process_callback)
        #    self.process_callback(mimic.get_defect())
        if entity_type == "f":
            mimic.register_fire_callback(self.process_callback)
        #    self.process_callback(mimic.get_fire())
        if entity_type == "s":
            mimic.register_sprinkler_callback(self.process_callback)
        #    self.process_callback(mimic.get_sprinkler())
        if entity_type == "z":
            mimic.register_zone_callback(self.process_callback)
        #    self.process_callback(mimic.get_zones())

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._is_on

    def process_callback(self, update):
        """Callback processor"""
        if self.entity_type != "z":
            self._is_on = update
        else:
            self._is_on = update[self.entity_index]

        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await self.async_base_added_to_hass()

    async def async_base_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        pass

    async def async_get_last_state(self):
        """Returns item state"""
        return self._is_on

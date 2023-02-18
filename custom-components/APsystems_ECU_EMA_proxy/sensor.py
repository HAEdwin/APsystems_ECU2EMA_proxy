"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging
LOGGER = logging.getLogger(__name__)

import socketserver
from socketserver import BaseRequestHandler
from datetime import datetime, timedelta
import threading

host = '172.16.0.19' #Your host IP-address here

class HTTPSERVER(BaseRequestHandler):
    def handle(self):
        rec = self.request.recv(1024)
        if rec:
            LOGGER.warning(f"Received: {rec}")
            send_str = "Thank you!"
            LOGGER.warning(f"Sending: {send_str}")
            self.request.send(send_str.encode('utf-8'))
            
def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([ExampleSensor()])

    listener_1 = socketserver.TCPServer((host, 5000), HTTPSERVER)
    thread_1 = threading.Thread(target=listener_1.serve_forever)
    listener_2 = socketserver.TCPServer((host, 5001), HTTPSERVER)
    thread_2 = threading.Thread(target=listener_2.serve_forever)
    LOGGER.warning("Proxy Started...")
    for threads in thread_1, thread_2:
        threads.start()

class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        # Fetch new state data for the sensor, this is the only method that should fetch new data for Home Assistant.
        LOGGER.warning("Sensor update...")
        self._attr_native_value = 23

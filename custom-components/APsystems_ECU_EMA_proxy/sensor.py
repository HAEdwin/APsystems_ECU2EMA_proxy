# Platform for sensor integration
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

# added
import socketserver
from socketserver import BaseRequestHandler
import threading
host = '172.16.0.19'
# end added

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None) -> None:

# added
    listener_1 = socketserver.TCPServer((host, 8995), HTTPSERVER)
    thread_1 = threading.Thread(target=listener_1.serve_forever)
    listener_2 = socketserver.TCPServer((host, 8996), HTTPSERVER)
    thread_2 = threading.Thread(target=listener_2.serve_forever)
    print('Proxy Started\nWaiting For Data... (use ctrl+c to stop)')
    for threads in thread_1, thread_2:
        threads.start()

    for threads in thread_1, thread_2:
        threads.join()
# end added

    # Set up the sensor platform
    add_entities([apsystems_ecu2ema_proxy()])


class apsystems_ecu2ema_proxy(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        # Fetch new state data for the sensor. This is the only method that should fetch new data for Home Assistant.
        LOGGER.warning("Sensor update")
        self._attr_native_value = 23
# added        
class HTTPSERVER(BaseRequestHandler):
    def handle(self):
        rec = self.request.recv(1024)
        if rec:
            try:
                LOGGER.warning(f"Received: {rec}")
            except:
                LOGGER.warning("Ignored unnecessary data")
# end added

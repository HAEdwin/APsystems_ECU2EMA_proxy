"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
#from homeassistant.const import TEMP_CELSIUS
from homeassistant.const import POWER_WATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)


import logging
LOGGER = logging.getLogger(__name__)

import socket
import socketserver
from socketserver import BaseRequestHandler
from datetime import datetime, timedelta
import threading

host = '172.16.0.19' #Your host IP-address here

class PROXYSERVER(BaseRequestHandler):
    def handle(self):
        (myhost, myport) = self.server.server_address
        global ecu_current_power
        rec = self.request.recv(1024)
        if rec:
            logging.warning(f"From ECU @{self.client_address[0]}:{myport} - {rec}")

            # Data to sensors
            if (rec[0:7].decode('ASCII')) == "APS18AA":
                ecu_current_power = int(rec[30:42])/100

            # forward message to EMA
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("3.67.1.32", myport)) # don't use ecu.apsystemsema.com due to rewrite it will loop
            sock.sendall(rec)

            # receive message from EMA    
            response = sock.recv(1024)
            logging.warning(f"From EMA: {response}\n")
            sock.close()

            # return message to ECU
            self.request.send(response)
            # Update local Sensor
            EMASensor.update(response)
            

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([EMASensor()])

    """Setup the listeners and threads."""
    listener_1 = socketserver.TCPServer((host, 8995), PROXYSERVER)
    thread_1 = threading.Thread(target=listener_1.serve_forever)
    listener_2 = socketserver.TCPServer((host, 8996), PROXYSERVER)
    thread_2 = threading.Thread(target=listener_2.serve_forever)
    listener_3 = socketserver.TCPServer((host, 8997), PROXYSERVER)
    thread_3 = threading.Thread(target=listener_3.serve_forever)
    for threads in thread_1, thread_2, thread_3:
        threads.start()
    LOGGER.warning("Proxy Started...")

class EMASensor(SensorEntity):
    """Representation of a Sensor."""
    _attr_name = "ECU Current Power"
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        # Fetch new state data for the sensor, this is the only method that should fetch new data for Home Assistant.
        #LOGGER.warning("Sensor update...")
        self._attr_native_value = ecu_current_power

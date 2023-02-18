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

import socket
import socketserver
from socketserver import BaseRequestHandler
from datetime import datetime, timedelta
import threading

host = '172.16.0.19' #Your host IP-address here

class HTTPSERVER(BaseRequestHandler):
    def handle(self):
        (myhost, myport) = self.server.server_address
        
        rec = self.request.recv(1024)
        if rec:
            LOGGER.warning(f"Received data on port: {myport} from ECU at: {self.client_address[0]} data: {rec}")
            send_str = "Thank you!"
            LOGGER.warning(f"Sending: {send_str}")
            self.request.send(send_str.encode('utf-8'))

# Dit is de client voor de connectie naar de EMA server met variabele poort
# aangeroepen met: client(ip, PORT, b'Hello World 1')
def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        LOGGER.warning(f"Received: {response}")
    finally:
        sock.close()

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
    listener_3 = socketserver.TCPServer((host, 5002), HTTPSERVER)
    thread_3 = threading.Thread(target=listener_3.serve_forever)
    for threads in thread_1, thread_2, thread_3:
        threads.start()
    LOGGER.warning("Proxy Started...")

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

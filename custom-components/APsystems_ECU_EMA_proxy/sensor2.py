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
import socket
import socketserver
from socketserver import BaseRequestHandler
import threading
host = "172.16.0.19"

def create_listen_socket(host, 8995):
    """ Setup the sockets our server will receive connection
    requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock

def recv_msg(sock):
    # Wait for data to arrive on the socket
    recvd = sock.recv(4096)
    LOGGER.warning (f"Received: {recvd}")
    return recvd

# end added



def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType | None = None) -> None:

    # Set up the sensor platform
    add_entities([apsystems_ecu2ema_proxy()])
    LOGGER.warning("2. Entities added...")
# added
#    listener_1 = socketserver.TCPServer((host, 8995), HTTPSERVER)
#    thread_1 = threading.Thread(target=listener_1.serve_forever)
#    listener_2 = socketserver.TCPServer((host, 8996), HTTPSERVER)
#    thread_2 = threading.Thread(target=listener_2.serve_forever)
#    LOGGER.warning("3. Proxy Started, waiting For Data...")
#    for threads in thread_1, thread_2:
#        threads.start()
#    LOGGER.warning("Threads started...")
#    for threads in thread_1, thread_2:
#        threads.join()
#    LOGGER.warning("Threads joined...")
    listen_sock = create_listen_socket(host, 8995)
    addr = listen_sock.getsockname()
    LOGGER.warning(f"Listening on: {.format(addr)}")
    while True:
        client_sock, addr = listen_sock.accept()
        LOGGER.warning(f"Connection from: {.format(addr)}")
        handle_client(client_sock, addr)
# end added


# added        
#class HTTPSERVER(BaseRequestHandler):
#    LOGGER.warning("1. HTTP Server...")
#    def handle(self):
#        rec = self.request.recv(1024)
#        if rec:
#            try:
#                LOGGER.warning(f"Received: {rec}")
#            except:
#                LOGGER.warning("Ignored unnecessary data")
# end added

class apsystems_ecu2ema_proxy(SensorEntity):
    # Representation of a Sensor

    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        # Fetch new state data for the sensor. This is the only method that should fetch new data for Home Assistant.
        LOGGER.warning("Sensor update")
        self._attr_native_value = 23


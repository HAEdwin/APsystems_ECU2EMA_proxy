# APsystems ECU2EMA Proxy

### &#x1F534; Warning: This integration is under construction and in very early stages - use at your own risk!

## Main purpose
The proxy will intercept traffic going from the ECU device to the EMA server and vice versa. Originally the basis was written to enable cloudless operation of the ECU and as a plan B for Kyle's apsystems_ecur integration. A proxy could be the ultimate solution for all ECU models including the ECU-3. For later models there are also ModBus compliant solutions to be found.

ToDo
- Interpret the data so that it can be set to sensors
- Use the checksum: verify the datalength (in cases of large PV installations) or enlarge the buffer size

## Prerequisites
- PiHole or AdGuard running as add-on installed on Home Assistant

## Installation
- If you haven't allready got one: Create a folder named "custom_components" in the config folder
- Create a subfolder in the custom_components folder called "apsystems_ecu2ema_proxy"
- Download the code and place it in the folder last mentioned
- Restart Home Assistant (important!)
- Add the following lines to your configuration.yaml
```
sensor:
  platform: apsystems_ecu2ema_proxy
```
- Restart Home Assistant once more and the proxy will load
- Finally: Use PiHole or AdGuard to rewrite DNS ecu.apsystemsema.com to your HA instance IP-addess
- Until now you'll find a data message from your ECU and the EMA server in the log every 5 minutes (when sun is up) or 15 minutes (when sun is down)

## How it works (more or less)
From what I know there are some data verifications build in to make sure data is complete and correct. After sunset these checks are performed every five minutes. When the datacheck is complete the communication takes place every 15 minutes. Around 03:00 in the morning firmware and maintenance checks are being done. Until sunset interval remains 15 minutes until the first inverter is up. This is the part we use/need.
When the inverter(s) are activated by the sun, data is sent to EMA on one of two randomly choosen ports 8995 and 8996 every five minutes. The EMA sites responds with a current timestamp minus 5 minutes to indicate all is well.
After three updates, the ECU initiates a "question" on what I think is the control port 8997. The EMA site responds with the registered ECU-ID and all is well. Then the cycle repeats at sundown.

## Where I need help
- Finding the purpose of data not yet mapped to current values

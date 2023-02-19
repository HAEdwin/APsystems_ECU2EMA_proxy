# APsystems ECU2EMA Proxy
## Main purpose
The proxy will intercept traffic going from the ECU device to the EMA server and vice versa. Intercepted data is being converted to sensors for use in Home Assistant. The data from the ECU is forwarded to the ecu.apsystemsema.com server. Returned data from the ecu.apsystemsema.com server will be forwarded to the ECU.

## Prerequisites
- PiHole or AdGuard

## Installation
Add the following line to your configuration.yaml
```
sensor:
  platform: apsystems_ecu2ema_proxy
```  
Use PiHole or AdGuard to rewrite DNS ecu.apsystemsema.com to your HA instance IP-addess



********* Notes for code ********************
Required: The MQTT broker service, either using the public or private(install needed: https://mosquitto.org/download/)

The code in this repo assumes you are using the local host method...
If using public connection, Caution - rate limits or slow traffic; replace localhost with "test.mosquitto.org"
Python: cli.connect("test.mosquitto.org", 1883)
VB: .WithTcpServer("test.mosquitto.org", 1883)

VB MQTT requires MQTTnet (version 3.1.2 or lower to work with this code) and MQTTnet.Extensions.ManagedClient (version 3.1.2 or lower) packages

This is an integrated mqtt.vb into uMD.gui which UMD.gui calles 
~~ Line edited is 1071 and 944


********* Troubleshoots and tracking **********************
- Need to test with getting continued data -> Need to check if it keeps connecting and reconnecting to the server

- Need to implement a voltage controller that uses moku api to change the voltage used for pizo (current)
Remote Voltage Control for Moku:Go via MQTT and VB.NET Bridge

This program enables remote control of a Moku:Go device to adjust output waveforms that control a piezoelectric device. It does so through a Python MQTT controller that communicates with a VB.NET GUI and interfaces directly with the Moku:Go using the Liquid Instruments Python SDK.

🔧 Features

Launches a VB.NET GUI executable to serve as the front-end controller

Uses MQTT messaging to receive commands from the GUI

Responds to the message "start_waveform" by:

Connecting to a Moku:Go device over USB-C or Ethernet

Sending a 1 Hz sine wave at 5 Vpp for 20 seconds

Then switching to a 10 Hz sine wave at 5 Vpp

📂 Project Structure

PYbridge/
├── mqtt.py                # Main Python controller logic
├── uMD_GUI.exe            # Compiled VB.NET GUI application

🧠 Purpose

The goal of this branch is to allow a remote system (GUI or command center) to control the output voltage waveform that is sent to a piezo actuator via the Moku:Go. This is useful in systems where precise waveform timing or remote adjustments are needed without direct manual control of the Moku.

⚙️ How It Works

The VB.NET app launches and publishes "start_waveform" via MQTT

The Python backend connects to the Moku:Go and sets the waveform

The waveform runs as described

✅ Requirements

Moku:Go connected via USB-C or Ethernet

Liquid Instruments Python SDK (pip install moku)

VB.NET compiled GUI in /bin/Debug/uMD_GUI.exe

MQTT broker running locally (localhost:1883)

🛠️ Notes

Uses force_connect=True to ensure ownership of Moku:Go

Calls set_defaults() to reset Moku state before output

Best used with Moku firmware version 601 and matching SDK bitstreams

⚠ If you see NoInstrumentBitstream, run:
moku download --fw_ver=601
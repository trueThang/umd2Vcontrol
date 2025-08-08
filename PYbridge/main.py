
import os
import sys
import time
import signal
import pandas as pd
from parse_data import To_Csv
from moku_device import Ctrl_Moku
from mqtt import Mqtt
stop_flag = False  # Global flag to indicate when to stop the program

#end signal handler for graceful exit
def handle_exit(signum, frame):
    global stop_flag
    print("\nExit signal received. Stopping gracefully...")
    stop_flag = True

signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # Termination

def main():
    """
    run mqtt that will open umd_gui.exe that will send data to python via mqtt
    moku will then connect to the moku device
    """
    mqtt = None
    moku = None

    try:

        #get data from VB.net and open measurement gui
        mqtt = Mqtt()

        #connect to moku and initalize
        moku = Ctrl_Moku()
        csv = To_Csv()
        
        if not mqtt or not moku: #check to see if mqtt and moku are initialized
            raise Exception("Failed to initialize MQTT or Moku connection.")
        
        initial_vpp = moku.set_voltage(5)
        data = mqtt.latest_value()  # Get the latest value from MQTT




    except Exception as e:
        print(f"error: {e}")
        sys.exit(0)



if __name__ == "__main__":
    main()
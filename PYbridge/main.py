
import os
import keyboard as ky
import sys
import time
import signal
import numpy as np
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

        if not mqtt or not moku: #check to see if mqtt and moku are initialized
            raise Exception("Failed to initialize MQTT or Moku connection.")
        
        off_set = 0.0
        control_max = 0.5
        control_min = -0.5
        start_time = time.time()
        initial_vpp = moku.set_voltage(off_set) #set voltage to 0 as default
        
        #------------ While getting data
        while not stop_flag: #while stop flag isnt triggered, keep getting data
            #ideal wave (sine)                  feq             t
            original_signal = np.sin(2 * np.pi * 1 * (time.time() - start_time))

            #get sensor wave data
            raw_data = mqtt.latest_value()  # Get the latest value from MQTT; 
            

        ##end of while

    except Exception as e:
        print(f"error in main.py: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
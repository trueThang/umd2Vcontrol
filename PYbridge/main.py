
import os
import queue
import sys
import time
import signal
import numpy as np
import pandas as pd
from mqtt import Mqtt
from collections import deque #rolling buffer
from parse_data import To_Csv
from moku_device import Ctrl_Moku
from controller import PID as pid, Low_PassFilter as lpf, Process_Data as process

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
        
        off_set = 0.0 #initial voltage offset
        buffer_size = 500
        #pid parameters
        Kp = 0.8
        Ki = 0.05
        Kd = 0.0
        
        buffer = deque(maxlen=buffer_size) #initalize buffer and set max rolling sample to 500
        initial_vpp = moku.set_voltage(off_set) #set voltage to 0 as default

        #initalize PID and low pass filter
        pid_controller = pid(Kp, Ki, Kd) 
        low_filter = lpf(alpha=0.1)
        process_data = process()  # Initialize the data processing class

        #------------ While getting data
        while not stop_flag: #while stop flag isnt triggered, keep getting data
            
            try:
                #get sensor wave data
                raw_data = mqtt.q.get(timeout=0.01)  # Get the latest value from MQTT; 
                buffer.append(raw_data) # Append the latest value to the buffer

                if len(buffer) == buffer_size:
                    #process the buffer to get scaled min/max
                    err = process_data.sine_process(buffer)  # Process the buffer to get the error value
                    off_set = low_filter.update(pid_controller.update(err))
                    moku.set_voltage(off_set) #update voltage offset


            except queue.Empty:
                pass

        #############end of while

    except Exception as e:
        print(f"error in main.py: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
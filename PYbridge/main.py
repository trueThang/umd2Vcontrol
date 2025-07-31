
import os
from pickle import INT
import sys
import time
import signal
import statistics as stats
import numpy as np
import threading as thread
from tracemalloc import stop
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
        curr_vpp = initial_vpp
        file = "data.csv" #ending in .csv
        status = True #for readbility
        csv.open_file(file)
        prev_data = 0.0
        THRESHOLD = 0
        INTERVAL = 50
        disp_points = np.array([])

        while not stop_flag: #loop until stop_flag is set

            #get data from message
            data = mqtt.latest_value()

            #if decoded data shows zero then skip to next iteration
            if data == 0.0 or data == 0:
                time.sleep(0.01)

                while status:
                    print("Zero detected...skippping...")
                    status = False
                    
                continue
            
            #put data into csv name file
            csv.write_file(file, data)
            
            
            
            disp_points.append(data)  # add data to array

            # adjusting length to be less than interval
            if (len(disp_points > INTERVAL)):
                disp_points = disp_points[1:]
            
            grad = np.gradient(disp_points) # get gradient of current points charted (at interval)
            print(f'Current gradient: {grad}, Threshold: {THRESHOLD}, Interval {INTERVAL}')


            if grad > THRESHOLD :

                # could be flawed for adjustment 
                if (grad > 0):
                    moku.set_voltage(curr_vpp := curr_vpp - 1.0)
                else:
                    moku.set_voltage(curr_vpp := curr_vpp + 1.0)
                

            

                



        #plot the data

    except Exception as e:
        print(f"error: {e}")
        sys.exit(0)

    finally:
        if os.path.exists(file):
            csv.calc_dis(file)
            print("Displacement calculated")



if __name__ == "__main__":
    main()





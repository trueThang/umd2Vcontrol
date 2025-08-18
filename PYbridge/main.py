
import os
import queue
import sys
import time
import signal
import numpy as np
from monitor import SineMonitor
from mqtt import Mqtt
from collections import deque #rolling buffer
#from parse_data import To_Csv
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
        buffer_vals = deque(maxlen=buffer_size)
        buffer_ts   = deque(maxlen=buffer_size)

        #pid parameters
        Kp = 0.8
        Ki = 0.05
        Kd = 0.0
        
        
        
        moku.set_waveform(
            channel=1,
            type_="Sine",
            amplitude = 5.0,   # Vpp; within 0.004..10 for Moku:Go
            frequency = 1.0,   # Hz; within 1e-3..20e6
            offset = 0.0,      # V; within -5..+5
        )

        monitor = SineMonitor(
            target_freq_hz=None,  # set to a value (ex: 5.0) if you know the desired frequency
            min_amp=0.3,          # amplitude threshold on normalized data
            r2_ok=0.90,           # fit quality threshold
            rmse_ok=0.20          # fit error threshold
        )

        last_report = time.time()  # Initialize previous time for timestamping

        #initalize PID and low pass filter
        pid_controller = pid(Kp, Ki, Kd) 
        low_filter = lpf(alpha=0.1)
        process_data = process()  # Initialize the data processing class

        #------------ While getting data
        while not stop_flag: #while stop flag isnt triggered, keep getting data
            
            try:
                #get sensor wave data
                item = mqtt.q.get(timeout=0.01)  # Get the latest value from MQTT; 
                if isinstance(item, tuple):
                    ts, raw_data = item

                else:
                    ts, raw_data = time.time(), item # Get the current timestamp if not provided

                buffer_vals.append(raw_data)
                buffer_ts.append(ts)

                # 2) drain burst
                while True:
                    try:
                        item = mqtt.q.get_nowait()
                        if isinstance(item, tuple):
                            ts, raw_data = item
                        else:
                            ts, raw_data = time.time(), item
                        buffer_vals.append(raw_data)
                        buffer_ts.append(ts)
                    except queue.Empty:
                        break

                # 3) process once
                if len(buffer_vals) == buffer_size:
                    # your existing processing -> error, PID, LPF, set_voltage
                    err = process_data.sine_process(buffer_vals)
                    pid_out  = pid_controller.update(err)
                    off_set  = low_filter.update(pid_out)
                    moku.set_voltage(off_set)

                    # 4) Sine health frequent 0.5
                    now = time.time()
                    if now - last_report > 0.5:
                        # Normalize window to -1,1 before fitting
                        w = np.array(buffer_vals, dtype=float)
                        w_min, w_max = float(w.min()), float(w.max())
                        
                        if w_max > w_min:
                            w_norm = (2.0*(w - w_min)/(w_max - w_min)) - 1.0
                        else:
                            w_norm = np.zeros_like(w)

                        metrics = monitor.analyze(np.array(buffer_ts, dtype=float), w_norm)
                        if metrics["ok"]:
                            print(f"[SINE OK] f~{metrics['f0']:.3f}Hz  R={metrics['R']:.2f}  R²={metrics['r2']:.3f}  RMSE={metrics['rmse']:.3f}  φ={metrics['phi']:.2f} rad")
                        else:
                            print(f"[SINE UNKNOWN]  f~{metrics.get('f0',0):.3f}Hz  R={metrics['R']:.2f}  R²={metrics['r2']:.3f}  RMSE={metrics['rmse']:.3f}")
                        
                        last_report = now


            except queue.Empty:
                pass

        #############end of while

    except Exception as e:
        print(f"error in main.py: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
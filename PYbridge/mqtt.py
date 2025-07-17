
import time
import threading
import subprocess
import paho.mqtt.client as mqtt
from moku.instruments import WaveformGenerator




class Mqtt():
    def __init__(self): 
        # Full path to your compiled VB.NET executable
        exe_path = r"C:\Users\thang\source\repos\moku_projects\uMD_GUI-30-Dec-7.29PM-20250316T042754Z-001\uMD_GUI-30-Dec-7.29PM\bin\Debug\uMD_GUI.exe"
        # Launch the .exe
        subprocess.Popen(exe_path)

        print("Python Side")
        self.cli = mqtt.Client()
        self.cli.on_connect, self.cli.on_message = self.on_connect, self.on_message
        self.cli.connect("localhost", 1883, 60)

        # Initialize Moku (Replace with your IP)
        self.moku_ip = "192.168.137.66"  #########Change this to your Moku's IP address
        if self.moku_ip == True:
            print("we found somthing")

        self.inst = WaveformGenerator(self.moku_ip)
        self.inst.set_defaults()

        #loop forever
        self.cli.loop_forever()

    def delay_search(self):
        print("Adjusting", end='', flush=True)
        for _ in range(3):
            time.sleep(0.7)
            print(".", end='',flush=True)

        print()##animated search... 

    def on_connect(self,cli, ud, flg, rc):
    
        connect = cli.subscribe("vb_to_py")
        if connect == 0:
            print("Python connected")


    def on_message(self, cli, ud, msg): #unloads what vb bridge sends -> then use it
        print("Recieved:")
        print(msg)
        data = msg.payload.decode()
        print(data)
        
        if data.strip().lower() == "start_waveform":
            threading.Thread(target=self.run_waveform_sequence).start()

    def run_waveform_sequence(self):
        print("Setting waveform: 1 Hz, 5 Vpp")
        self.inst.generate_waveform(channel=1, type='Sine', amplitude=2.5, frequency=1, offset=0.0)
        time.sleep(20)
        print("Switching waveform: 10 Hz, 5 Vpp")
        self.inst.generate_waveform(channel=1, type='Sine', amplitude=2.5, frequency=10, offset=0.0)


if __name__=="__main__":
    Mqtt()


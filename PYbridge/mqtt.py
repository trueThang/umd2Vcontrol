
import time
import threading
import subprocess #to run the VB.NET executable
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
        self.moku_ip = "192.168.73.1"  #########Change this to your Moku's IP address
        if self.moku_ip:
            print(f"Connected to the IP: {self.moku_ip}")

        self.inst = WaveformGenerator(self.moku_ip, force_connect=True ) #get the instrument instance
        self.inst.set_defaults() #resets waveform to factory defined initial configuration
        threading.Thread(target=self.run_waveform_sequence).start()
        
        #loop forever
        self.cli.loop_forever()

    def on_connect(self,cli, ud, flg, rc):
    
        connect = cli.subscribe("vb_to_py")
        if connect == 0:
            print("Python connected")


    def on_message(self, cli, ud, msg): #unloads what vb bridge sends -> then use it
        #print("Recieved:")
        #print(f"payload recieved: {msg}")
        data = msg.payload.decode()

        #check if data is numeric
        try:
            num = float(data)
            #print(f"encoded data: {data}\n")
            #threading.Thread(target=self.run_waveform_sequence).start()
            
        except ValueError:
            print("Received non-numeric data, ignoring...")


    def run_waveform_sequence(self): #testing to see if api works, not controlling vpp yet
        print("Setting waveform: 10 Hz, 1 Vpp")

        self.inst.generate_waveform(channel=1, type='Sine', amplitude=1, frequency=10, offset=0.0)
        time.sleep(20)

        print("Switching waveform: 10 Hz, 5 Vpp")
        self.inst.generate_waveform(channel=1, type='Sine', amplitude=5, frequency=10, offset=0.0)

        def close(self): #tells moku to disconnect for programs that doesn't force conenct
            self.inst.close()

if __name__=="__main__":
    Mqtt()


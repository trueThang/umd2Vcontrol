#not implemented yet
import time
from moku.instruments import WaveformGenerator


class Ctrl_Moku():
    """
    This class will call moku api to change the voltage of the pizo
    """
    def __init__(self): # constructor
        try:
            self.ip= "192.168.73.1"
            #self.ip = input("Enter Moku IP address: ") #get IP

            self.connect() # initialize connection to Moku device

        except Exception as e:
            print(f"Error connecting to Moku device: {e}")
            self.inst = None

        

    def connect(self):
        """
        Connect to the Moku device
        """
            
        self.inst = WaveformGenerator(self.ip, force_connect=True)  # Initialize the instrument with the Moku's IP address
        self.inst.set_defaults()  # Reset waveform to factory defined initial configuration

        
    def set_voltage(self, vpp):
        print(f"Setting waveform: {vpp} Vpp")

        self.inst.generate_waveform(channel=1, type='Sine', amplitude=vpp, frequency=10, offset=0.0)
        

    def disconnect(self): #tells moku to disconnect for programs that doesn't force conenct
        self.inst.close()
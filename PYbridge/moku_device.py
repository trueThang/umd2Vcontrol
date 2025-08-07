#not implemented yet
import time
from moku.instruments import WaveformGenerator



class Ctrl_Moku():
    """
    This class will call moku api to change the voltage of the pizo
    """
    def __init__(self): # constructor
        self.ip= "192.168.73.1"
        #self.ip = input("Enter Moku IP address: ") #get IP

        #parameters
        self.AMP = 5
        self.FREQ = 1
        self.WAVE = "Sine"
            
        self.try_connect = self.connect() # initialize connection to Moku device   


    def connect(self):
        """
        Connect to the Moku device
        """
        try:
            self.inst = WaveformGenerator(self.ip, force_connect=True)  # Initialize the instrument with the Moku's IP address
            print("Connected to Moku")  
            self.inst.set_defaults()  # Reset waveform to factory defined initial configuration 

        except Exception as e:
            print(f"Error connecting to Moku device: {e}")
            self.inst = None
        
    def set_voltage(self, dc_level):
        try:

            self.inst.generate_waveform(channel=1, type=self.WAVE, amplitude=self.AMP, frequency=self.FREQ, offset=dc_level)
            print(f"Setting Amplitude: {dc_level} V")

        except Exception as e:
            print(f"Error:{e}")
    
    #recieves time, offset, measured
    def pid_controller(self):
        pass


    def disconnect(self): #tells moku to disconnect for programs that doesn't force conenct
        pass


    #for safety, use context manager to ensure proper cleanup if used with a 'with' statement
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback): 
        self.disconnect()

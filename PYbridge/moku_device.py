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
        
    def set_voltage(self, vpp):
        try:
            #note : vpp is peak to peak voltage, not amplitude so divide by 2 to get amplitude
            amp = vpp

            self.inst.generate_waveform(channel=1, type='Sine', amplitude=amp, frequency=1, offset=0.0)
            print(f"Setting Amplitude: {amp} Vpp")

        except Exception as e:
            print(f"Error:{e}")
    
    def disconnect(self): #tells moku to disconnect for programs that doesn't force conenct
        pass


    #for safety, use context manager to ensure proper cleanup if used with a 'with' statement
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback): 
        self.disconnect()

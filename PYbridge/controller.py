#not implemented yet

from moku.instruments import WaveformGenerator


class Ctrl_Moku():
    """
    This class will call moku api to change the voltage of the pizo
    """
    def __init__(self, data): # constructor
        self.waveform = self.connect() # initialize connection to Moku device
        print(self.waveform)

    def connect(self):
        """
        Connect to the Moku device
        """
        try: 
            #ip = input("Enter Moku IP address: ")
            ip= "192.168.137.66"
            self.inst = WaveformGenerator(ip)  # Initialize the instrument with the Moku's IP address
            self.inst.set_defaults()  # Reset waveform to factory defined initial configuration

        except Exception as e:
            print(f"Error connecting to Moku device: {e}")
            self.inst = None

    def set_voltage(self):
        pass
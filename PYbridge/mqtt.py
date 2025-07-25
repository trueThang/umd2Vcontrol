
import subprocess #to run the VB.NET executable
import paho.mqtt.client as mqtt





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
       
        #loop forever
        self.cli.loop_forever()

    def on_connect(self,cli, ud, flg, rc):
    
        connect = cli.subscribe("vb_to_py")
        if connect == 0:
            print("Python connected")


    def on_message(self, cli, ud, msg): #unloads what vb bridge sends -> then use it
        data = msg.payload.decode()

        #check if data is numeric
        try:
            num = float(data)
            print(f"encoded data: {num}\n") #shows the numeric data received for checking
            
        except ValueError:
            print("Received non-numeric data, ignoring...")


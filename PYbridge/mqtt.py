
import time
import paho.mqtt.client as mqtt

class Mqtt():
    def __init__(self): #controller
    
        print("Python Side")
        self.cli = mqtt.Client()
        self.cli.on_connect, self.cli.on_message = self.on_connect, self.on_message
        self.cli.connect("localhost", 1883, 60)
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
    


if __name__=="__main__":
    Mqtt()


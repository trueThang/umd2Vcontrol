
import time
import paho.mqtt.client as mqtt

def main():
    
    print("Python Side")
    cli = mqtt.Client()
    cli.on_connect, cli.on_message = on_connect, on_message
    cli.connect("localhost", 1883, 60)
    cli.loop_forever()

def delay_search():
    print("Adjusting", end='', flush=True)
    for _ in range(3):
        time.sleep(0.7)
        print(".", end='',flush=True)

    print()##animated search... 

def on_connect(cli, ud, flg, rc):
    
    connect = cli.subscribe("vb_to_py")
    if connect == True:
        print("Python connected")


def on_message(cli, ud, msg): #unloads what vb bridge sends -> then use it
    print("Recieved:")
    print(msg)
    data = msg.payload.decode()
    print(data)
    


if __name__=="__main__":
    main()


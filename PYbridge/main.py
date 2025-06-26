import time
import paho.mqtt.client as mqtt

def main():
    ''''''''
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
    cli.subscribe("vb_to_py")

def on_message(cli, ud, msg):
    print("VB says:", msg.payload.decode())
    delay_search()
    #cli.publish("py_to_vb", f"ACK {msg.payload.decode()}")
    text = "Adjusted Voltage!"
    print(text)
    cli.publish("py_to_vb", text)



if __name__=="__main__":
    main()


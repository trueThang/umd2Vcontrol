moku IP: 192.168.73.1


------- Future Improvements

Add waveform parameter customization (frequency, duration, amplitude)

Implement graceful disconnection using inst.close()

Support multiple commands or waveform types

create a main to run : mqtt, gui for pid, voltage control

------- Notes


import math
import time
from mqtt import Mqtt  # your class that receives VB displacement

# control parameters
AMPLITUDE = 5.0           # target displacement in microns
FREQ = 1.0                # Hz
GAIN = 0.2                # simple proportional gain
OFFSET = 0.0              # for DC offset of sine wave

def target_sine(t):
    return AMPLITUDE * math.sin(2 * math.pi * FREQ * t) + OFFSET

# main loop

mqtt_bridge = Mqtt()
start_time = time.time()

try:
    while True:
        t = time.time() - start_time
        setpoint = target_sine(t)

        measured = mqtt_bridge.get_latest()
        if measured is not None:
            error = setpoint - measured
            correction = GAIN * error
            new_voltage = OFFSET + correction

            # safety clamp to prevent overdrive
            new_voltage = max(min(new_voltage, 10.0), -10.0)

            print(f"[{t:.2f}s] set: {setpoint:.3f}  measured: {measured:.3f}  → voltage: {new_voltage:.3f}")

            # TODO: send this to Moku
            # e.g., moku.set_output_voltage(new_voltage)

        else:
            print("Waiting for displacement...")

        time.sleep(0.01)  # 100 Hz

except KeyboardInterrupt:
    print("Stopped.")

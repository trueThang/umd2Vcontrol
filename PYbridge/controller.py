from calendar import c
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class PID():
    """
    A simple PID controller implementation.
    returns the control output based on the ERROR input.
    """
    def __init__(self, Kp=0.8, Ki=0.05, Kd=0.0): 
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.integral = 0
        self.prev_error = 0

    def update(self, error):
        self.integral += error
        derivative = error - self.prev_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return output


class Low_PassFilter(): 
    """
    used to remove noise from the sensor data

    alpha = 0.9 fast response, light smoothing
    alpha = 0.1 slow response, heavy smoothing
    default is larger smoothing
    """
    def __init__(self, alpha=0.1):
        self.alpha = alpha  # smoothing factor (0 < alpha < 1)
        self.filtered = 0

    def update(self, new_value):
        self.filtered = self.alpha * new_value + (1 - self.alpha) * self.filtered
        return self.filtered

class Process_Data():
    """
    Process the raw data from the sensor.
    """

    def __init__(self):
        pass

    def sine_process(self, buffer):

        df = pd.DataFrame(list(buffer), columns=['Raw']) # Convert buffer to DataFrame
        scaler = MinMaxScaler(feature_range=[-1,1]) # Scale data between -1 and 1
        df['normalized'] = scaler.fit_transform(df[['Raw']])

        #make sine wave
        x = np.linspace(0, 2 * np.pi, len(buffer))
        df['sine'] = np.sin(x)

        #error between normalized and sine wave
        df['error'] = df['normalized'] - df['sine']

        current_error = df['error'].iloc[-1] #get the latest error value

        return float(current_error)


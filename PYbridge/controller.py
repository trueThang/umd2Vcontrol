
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class PID():
    """
    PID controller with simple anti-windup and output clamps.
    Returns the control output based on the ERROR input.
    """
    def __init__(self, Kp=0.8, Ki=0.05, Kd=0.0,
                 out_min=-5.0, out_max=5.0,    # hardware-safe default; adjust to your device
                 i_min=-50.0, i_max=50.0):     # integral clamp to avoid wind-up
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.integral = 0.0
        self.prev_error = 0.0
        self.out_min, self.out_max = out_min, out_max
        self.i_min, self.i_max = i_min, i_max
        self.last_output = 0.0

    def update(self, error):
        # derivative
        derivative = error - self.prev_error

        # tentative integral update (apply conditional integration for anti-windup)
        tentative_integral = self.integral + error

        # compute unconstrained output using tentative integral
        unconstrained = self.Kp * error + self.Ki * tentative_integral + self.Kd * derivative

        # if output would saturate and error would push further into saturation, don't integrate
        would_saturate_high = unconstrained > self.out_max and error > 0
        would_saturate_low  = unconstrained < self.out_min and error < 0
        if not (would_saturate_high or would_saturate_low):
            self.integral = max(self.i_min, min(self.i_max, tentative_integral))

        # final output with actual integral
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        # clamp to hardware range
        output = max(self.out_min, min(self.out_max, output))

        self.prev_error = error
        self.last_output = output
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
    Process the raw data from the sensor to produce a tracking error
    against a reference sine wave.
    """

    def __init__(self, cycles_per_window=1.0, target_freq_hz=None, eps=1e-9):
        self.cycles_per_window = cycles_per_window
        self.target_freq_hz = target_freq_hz
        self.eps = eps

    def sine_process(self, buffer):

        df = pd.DataFrame(list(buffer), columns=['Raw'])

        # Guard: if window is effectively flat, return 0 error to avoid blowing up PID
        rmin, rmax = float(df['Raw'].min()), float(df['Raw'].max())
        if abs(rmax - rmin) < self.eps:
            return 0.0

        # Normalize to [-1, 1] within the window
        scaler = MinMaxScaler(feature_range=(-1, 1))
        df['normalized'] = scaler.fit_transform(df[['Raw']])

        # Build sine reference; default = 1 cycle per window (same as your existing behavior)
        N = len(df)
        x = np.linspace(0, 2 * np.pi * self.cycles_per_window, N)
        df['sine'] = np.sin(x)

        # Error = latest normalized value minus latest sine value
        current_error = float(df['normalized'].iloc[-1] - df['sine'].iloc[-1])
        return current_error


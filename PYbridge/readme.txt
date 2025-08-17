moku IP: 192.168.73.1


------- Future Improvements

Add waveform parameter customization (frequency, duration, amplitude)

Implement graceful disconnection using inst.close()

Support multiple commands or waveform types

create a main to run : mqtt, gui for pid, voltage control

------- Notes


import numpy as np
import matplotlib.pyplot as plt

# --- Simulation parameters ---
fs = 1000  # Hz
t_end = 2  # seconds
t = np.linspace(0, t_end, int(fs * t_end))
freq = 1  # Hz for the sine wave

# Original signal (ideal)
original_signal = np.sin(2 * np.pi * freq * t)

# Deviated signal (distorted by phase lag + noise)
phase_lag = 0.05  # smaller lag
noise_amp = 0.05
np.random.seed(42)
deviated_signal = np.sin(2 * np.pi * freq * (t - phase_lag)) + noise_amp * np.random.randn(len(t))

# --- PID parameters ---
Kp = 0.8      # smaller proportional gain
Ki = 0.05     # small integral gain
Kd = 0.0      # zero derivative gain
tau_d = 0.01  # derivative filter (not used here)
tau_ctrl = 0.1  # larger smoothing for control output

# Control output limits
control_min = -0.5
control_max = 0.5

# --- Initialize variables ---
dt = 1 / fs
integral = 0.0
prev_error = 0.0
prev_derivative = 0.0
prev_control = 0.0
corrected_signal = np.zeros_like(t)

# --- PID loop ---
for i in range(len(t)):
    error = original_signal[i] - deviated_signal[i]

    # Integral term with simple anti-windup
    integral += error * dt
    integral = np.clip(integral, -1, 1)

    # Derivative (not used here, set zero)
    raw_derivative = (error - prev_error) / dt
    derivative = 0

    # PID control
    control_raw = Kp * error + Ki * integral + Kd * derivative

    # Limit control output
    control_raw = np.clip(control_raw, control_min, control_max)

    # Low-pass filter control output
    control = (tau_ctrl / (tau_ctrl + dt)) * prev_control + (dt / (tau_ctrl + dt)) * control_raw

    # Apply correction
    corrected_signal[i] = deviated_signal[i] + control

    # Store previous values
    prev_error = error
    prev_control = control

# --- Plot results ---
plt.figure(figsize=(10, 6))
plt.plot(t, original_signal, label="Original Signal", linewidth=2)
plt.plot(t, deviated_signal, label="Deviated Signal", alpha=0.7)
plt.plot(t, corrected_signal, label="Corrected Signal (PID + Filters)", linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("PID Correction of Deviated Signal (Full Sine Cycle)")
plt.legend()
plt.grid(True)
plt.show()
#"""
# -------- How-to read----------------------------------------------------------------------
#| When the stream is sine-like, you’ll see periodic [SINE OK]                              |
#|  lines with high R^2, (~1.0), low RMSE (~0), stable f0, and a reasonable amplitude R.    |
#|                                                                                          |
#| If the sensor/plant isn’t behaving, you’ll see [SINE Unkown]                             |
#|  and which metric failed (low R^2, high RMSE, tiny R).                                   |
# ------------------------------------------------------------------------------------------
#"""

# monitor.py
import numpy as np

class SineMonitor:
    """
    Online sinusoid detector on a rolling window.
    If target_freq_hz is None, it estimates the best frequency by FFT.
    """
    def __init__(self, target_freq_hz=None, min_amp=0.3, r2_ok=0.90, rmse_ok=0.20):
        self.target_freq_hz = target_freq_hz
        self.min_amp = min_amp
        self.r2_ok = r2_ok
        self.rmse_ok = rmse_ok

    def _fit_fixed_freq(self, t, y, f0):
        """
        Returns amplitude R, phase phi, dc, yhat, rmse, r2.
        """
        w = 2*np.pi*f0
        S = np.sin(w*t)
        C = np.cos(w*t)
        X = np.column_stack([S, C, np.ones_like(t)])
        # least-squares solve
        theta, *_ = np.linalg.lstsq(X, y, rcond=None)
        a, b, c = theta
        yhat = X @ theta
        resid = y - yhat
        rmse = float(np.sqrt(np.mean(resid**2)))
        ss_tot = float(np.sum((y - np.mean(y))**2)) + 1e-12
        r2 = 1.0 - float(np.sum(resid**2))/ss_tot
        R = float(np.sqrt(a*a + b*b))
        phi = float(np.arctan2(b, a))  
        return R, phi, c, yhat, rmse, r2

    def _estimate_freq_fft(self, t, y):
        """
        Rough frequency estimate from FFT assuming near uniform
        """
        # infer fs from median dt
        dt = np.median(np.diff(t))
        fs = 1.0/dt if dt > 0 else 1.0
        Y = np.fft.rfft(y - np.mean(y))
        freqs = np.fft.rfftfreq(len(y), d=dt)
        # ignore DC bin
        if len(freqs) <= 1:
            return None, fs
        mag = np.abs(Y)
        mag[0] = 0.0
        k = int(np.argmax(mag))
        return float(freqs[k]), fs

    def analyze(self, t, y):
        """
        t: 1D array of timestamps (seconds) or sample indices
        y: 1D array of window samples
        Returns dict with metrics and a boolean 'is_sinusoid'.
        """
        t = np.asarray(t, dtype=float)
        y = np.asarray(y, dtype=float)

        # choose frequency
        f0 = self.target_freq_hz
        if f0 is None:
            f0, fs = self._estimate_freq_fft(t, y)
            if f0 is None or f0 <= 0:
                return {"ok": False, "reason": "no_freq", "R":0, "phi":0, "dc":float(np.mean(y)),
                        "rmse":1.0, "r2":0.0, "f0":0.0}
        R, phi, dc, yhat, rmse, r2 = self._fit_fixed_freq(t, y, f0)

        ok = (R >= self.min_amp) and (r2 >= self.r2_ok) and (rmse <= self.rmse_ok)

        #  ratio peak/non-peak (spec purity)
        # 
        return {
            "ok": ok, "R": R, "phi": phi, "dc": dc,
            "rmse": rmse, "r2": r2, "f0": f0
        }







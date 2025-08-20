
from moku.instruments import WaveformGenerator



class Ctrl_Moku():
    """
    This class will call moku api to change the voltage of the pizo
    """
    def __init__(self):
        self.ip = "192.168.73.1"

        # Desired waveform defaults (you can override from main)
        self.CHANNEL = 1
        self.WAVE    = "Sine"     # allowed: Off, Sine, Square, Ramp, Pulse, DC, Noise
        self.AMP_VPP = 5.0        # Vpp (0.004 .. 10 for Moku:Go)
        self.FREQ_HZ = 1.0        # Hz  (1e-3 .. 20e6 for Moku:Go)
        self.OFFSET  = 0.0        # V   (-5 .. +5)

        # Hard safety clamps from API limits (Moku:Go)
        self.AMP_MIN, self.AMP_MAX       = 0.004, 10.0
        self.FREQ_MIN, self.FREQ_MAX     = 1e-3, 20e6
        self.OFFSET_MIN, self.OFFSET_MAX = -5.0, 5.0

        self.try_connect = self.connect()   


    def connect(self):
        try:
            self.inst = WaveformGenerator(self.ip, force_connect=True)
            print("Connected to Moku")
            self.inst.set_defaults()  # reset instrument
            # Prefer HiZ termination when driving a high-impedance load to achieve full Vpp/offset
            try:
                self.inst.set_output_termination(channel=self.CHANNEL, termination="HiZ")
            except Exception as e:
                print(f"Warning: set_output_termination not applied: {e}")
        except Exception as e:
            print(f"Error connecting to Moku device: {e}")
            self.inst = None

    def _clamp(self, v, vmin, vmax):
        return max(vmin, min(vmax, float(v)))

    def set_waveform(self, channel=None, type_=None, amplitude=None, frequency=None, offset=None, phase=None):
        """
        Configure the generator following API parameter semantics:
        - amplitude is Vpp, frequency in Hz, offset in V, phase in degrees.
        """
        if self.inst is None:
            print("Moku not connected; skipping set_waveform.")
            return

        ch   = channel   if channel   is not None else self.CHANNEL
        typ  = type_     if type_     is not None else self.WAVE
        amp  = amplitude if amplitude is not None else self.AMP_VPP
        freq = frequency if frequency is not None else self.FREQ_HZ
        ofs  = offset    if offset    is not None else self.OFFSET

        amp  = self._clamp(amp,  self.AMP_MIN,  self.AMP_MAX)
        freq = self._clamp(freq, self.FREQ_MIN, self.FREQ_MAX)
        ofs  = self._clamp(ofs,  self.OFFSET_MIN, self.OFFSET_MAX)

        kwargs = dict(channel=ch, type=typ, amplitude=amp, frequency=freq, offset=ofs)
        if phase is not None:
            # phase allowed 0..360 deg per docs
            kwargs["phase"] = float(phase)

        try:
            self.inst.generate_waveform(**kwargs)  # conforms to API
            print(f"Waveform set: ch={ch}, type={typ}, amp(Vpp)={amp}, freq(Hz)={freq}, offset(V)={ofs}" + (f", phase={kwargs.get('phase')}" if "phase" in kwargs else ""))
        except Exception as e:
            print(f"Error in generate_waveform: {e}")

    def set_voltage(self, dc_level):
        """
        Your PID drives 'offset'. Keep amplitude/frequency constant,
        only update 'offset' within [-5, +5] V
        """
        self.set_waveform(offset=dc_level)

    def disconnect(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

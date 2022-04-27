class Waveform:
    """
    Class representing single waveform: a shape on one of the buses.
    Therefore should contain information such as: bus, values and timestamps.
    """
    def __init__(self,
                 bus,
                 values,
                 timestamps):
        self.bus = bus
        self.values = values
        self.timestamps = timestamps

    @property
    def start_time(self):
        return self.timestamps[0]

    @property
    def end_time(self):
        return self.timestamps[-1]

    def __str__(self):
        return f"Waveform object, bus: {self.bus}, values: {self.values}, timestamps: {self.timestamps}."

class HistogramsCalculatorConfig:
    def __init__(self, bins_no=None, bus_to_min_max=None):
        """

        Parameters
        ----------
        bins_no
            Number of bins that will be used to create histograms of current waveforms values.
        bus_to_min_max
            Range used to calculate histograms.
        """
        self.bins_no = bins_no if bins_no else {
            "K1": 15,
            "K2": 15,
            "K3": 15,
            "K4": 15
        }
        self.bus_to_min_max = bus_to_min_max if bus_to_min_max else {
            "K1": (0, 800),
            "K2": (0, 1200),
            "K3": (0, 700),
            "K4": (0, 500)
        }
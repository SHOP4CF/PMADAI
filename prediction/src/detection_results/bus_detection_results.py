class BusDetectionResult:
    """
    This class stores information about the detection result on a single bus.

    Attributes
    ----------
    not_normalized_score
        Float: not normalized model response on a single bus.
    normalized_score
        Float: normalized model response score on a single bus.
    threshold
        Float: Threshold for determining the occurrence of an anomaly.
    normalized_threshold
        Float: Normalized threshold for determining the occurrence of an anomaly.
    """
    def __init__(self, not_normalized_score: float, normalized_score: float, threshold: float,
                 normalized_threshold: float):
        self.not_normalized_score: float = not_normalized_score
        self.normalized_score: float = normalized_score
        self.threshold: float = threshold
        self.normalized_threshold: float = normalized_threshold

    @property
    def anomaly(self) -> bool:
        """
        Boolean: information as to whether the bus contains an anomalous waveform.
        """
        return bool(self.normalized_score > self.normalized_threshold)

    def __str__(self):
        return f'BusDetectionResult(not_normalized_score={self.not_normalized_score},' \
               f'normalized_score={self.normalized_score},' \
               f'threshold={self.threshold},' \
               f'normalized_threshold={self.normalized_threshold},' \
               f'anomaly={self.anomaly})'

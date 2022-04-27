from src.detection_results import BusDetectionResult
from typing import Mapping
from collections import defaultdict
from src.config_reader import config


class DetectionResult:
    """
    This class is responsible for storing results for each single bus and for computing the final result based on
    components in the 'BusDetectionResult' form.

    Attributes
    -----------
    k1_result
        BusDetectionResult: detection result on the first bus.
    k2_result
        BusDetectionResult: detection result on the second bus.
    k3_result
        BusDetectionResult: detection result on the third bus.
    k4_result
        BusDetectionResult: detection result on the fourth bus.
    normalized_score
        Float: normalized global detection result.
    score
        Float: not normalized global detection result.
    anomaly
        Boolean: true if waveform is anomalous.
    """

    def __init__(self, k1_result: BusDetectionResult, k2_result: BusDetectionResult,
                 k3_result: BusDetectionResult, k4_result: BusDetectionResult):
        self.k1_result: BusDetectionResult = k1_result
        self.k2_result: BusDetectionResult = k2_result
        self.k3_result: BusDetectionResult = k3_result
        self.k4_result: BusDetectionResult = k4_result
        self.normalized_score: float = 0.0
        self.score: float = 0.0
        self.anomaly: bool = False
        self.aggregate()

    @classmethod
    def single_model_result(cls, buses_results: Mapping[str, BusDetectionResult]):
        """
        This method is used when only one type of model were used.
        In this case, aggregation of the results of the different models is not necessary.

        Parameters
        ----------
        buses_results
            Dictionary containing BusDetectionResult for each bus.

        Returns
        -------
        Instance its own class with information about detection result.
        """
        return cls(
            **buses_results
        )

    @classmethod
    def multiple_models_result(cls, buses_results: Mapping[str, Mapping[str, BusDetectionResult]]):
        """
        This method is used when more than one type of model were used.
        In this case, aggregation of the results of the different models is necessary and before passing parameters
        to class init, aggregation is performed.

        Parameters
        ----------
        buses_results
            Dictionary containing BusDetectionResult for each bus for each model types.

        Returns
        -------
        Instance its own class with information about detection result.
        """
        aggregated_buses_results = cls.aggregate_multiple_results_as_weighted_average(buses_results)
        return cls(
            **aggregated_buses_results
        )

    def aggregate(self):
        """
        This method is called during instance initialization. Global result is computed based on buses results.
        """
        for bus_result in [self.k1_result, self.k2_result, self.k3_result, self.k4_result]:
            self.normalized_score = max(bus_result.normalized_score, self.normalized_score)
            self.score = max(bus_result.not_normalized_score, self.score)
            self.anomaly = bus_result.anomaly or self.anomaly

    @staticmethod
    def aggregate_multiple_results_as_weighted_average(buses_results: Mapping[str, Mapping[str, BusDetectionResult]]) -> \
            Mapping[str, BusDetectionResult]:
        """
        This method aggregate the results of each model into one global response.
        Aggregation is performed as weighted average response of each model. Weights are taken from the
        configuration file. If this mean is greater than averaged threshold
        the waveform is recognised as anomaly.

        Parameters
        ----------
        buses_results
            Dictionary containing BusDetectionResult for each bus for each model types.

        Returns
        -------
        buses_detection
            Dictionary containing aggregated and normalized BusDetectionResult for each bus.
        """
        buses_detection = defaultdict(lambda: BusDetectionResult(0.0, 0.0, 0.0, 0.0))
        models_weights = config['models']['aggregation_weights']
        sum_of_weights = sum([weight for weight in models_weights.values()])
        for model_type, model_results in buses_results.items():
            weight = models_weights[model_type.lower()]
            for bus, bus_result in model_results.items():
                buses_detection[bus].normalized_score += (bus_result.normalized_score * weight) / sum_of_weights
                buses_detection[bus].not_normalized_score += (bus_result.not_normalized_score * weight) / sum_of_weights
                buses_detection[bus].normalized_threshold += (bus_result.normalized_threshold * weight) / sum_of_weights
                buses_detection[bus].threshold += (bus_result.threshold * weight) / sum_of_weights
        return buses_detection

    def to_dict(self):
        return {
            'score': self.normalized_score,
            'anomaly': self.anomaly,
            'K1': {
                'score': self.k1_result.normalized_score,
                'anomaly': self.k1_result.anomaly
            },
            'K2': {
                'score': self.k2_result.normalized_score,
                'anomaly': self.k2_result.anomaly
            },
            'K3': {
                'score': self.k3_result.normalized_score,
                'anomaly': self.k3_result.anomaly
            },
            'K4': {
                'score': self.k4_result.normalized_score,
                'anomaly': self.k4_result.anomaly
            }
        }

    def __str__(self):
        return str(self.to_dict())

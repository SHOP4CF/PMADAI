import pytest
from math import isclose

from src.detection_results import detection_result, bus_detection_results


@pytest.mark.detection_results
@pytest.mark.parametrize('not_normalized_score, normalized_score, threshold, normalized_threshold',
                         [(2, 0.8, 1, 0.5),
                          (2, 0.8, 3, 0.9),
                          (2, 0.8, 2, 0.8)
                          ]
                         )
def test_single_bus_anomaly(not_normalized_score, normalized_score, threshold, normalized_threshold):
    """
    This test check if class which holds results with respect to specific bus correctly obtain anomaly.
    It is parametrized by every possible situation: anomalous waveform, not anomalous waveform with value
    significantly lower than threshold and not anomalous waveform with value equals threshold (corner case).
    All anomaly are checked on normalized and regular score and both of results have to be compatible.
    """
    bus_result = bus_detection_results.BusDetectionResult(
        not_normalized_score=not_normalized_score,
        normalized_score=normalized_score,
        threshold=threshold,
        normalized_threshold=normalized_threshold
    )
    assert (bus_result.anomaly == (normalized_score > normalized_threshold)) and \
           (bus_result.anomaly == (not_normalized_score > threshold))


@pytest.mark.detection_results
@pytest.mark.parametrize('bus_results_dict_with_highest_score_on_first_bus', [
    ({
        'not_normalized_score': 2,
        'normalized_score': 0.8,
        'threshold': 1,
        'normalized_threshold': 0.5,
        'constant_subtracted': 0.2
    }),
    ({
        'not_normalized_score': 2,
        'normalized_score': 0.8,
        'threshold': 3,
        'normalized_threshold': 0.9,
        'constant_subtracted': 0.2
    }),
    ({
        'not_normalized_score': 2,
        'normalized_score': 0.8,
        'threshold': 2,
        'normalized_threshold': 0.8,
        'constant_subtracted': 0.2
    })
], indirect=True)
def test_single_model_result_with_highest_score_on_first_bus(bus_results_dict_with_highest_score_on_first_bus):
    """
    This test cover situation when single model is used to obtain the anomaly result.
    Data are prepared in a way where anomaly highest prediction score occur on a first bus.
    The assumption of aggregation is that the final score is the maximum value over all buses so
    in this case global score should be equal score on bus 1. Anomaly also should occur if bus one is anomalous.
    """
    bus_results = bus_results_dict_with_highest_score_on_first_bus
    detection_results = detection_result.DetectionResult.single_model_result(bus_results)
    assert detection_results.normalized_score == bus_results['k1_result'].normalized_score
    assert detection_results.score == bus_results['k1_result'].not_normalized_score
    assert detection_results.anomaly == bus_results['k1_result'].anomaly


@pytest.mark.detection_results
@pytest.mark.parametrize('aggregation_weights', [(0.5, 0.5), (0.9, 0.1), (0.1, 0.9), (2, 1)], indirect=True)
def test_multiple_models_results_with_aggregation_weights(autoencoder_bus_results,
                                                          isolationforest_bus_results,
                                                          aggregation_weights):
    """
    This test cover situation when two models are used to get the final response about anomaly.
    Final results is an aggregation over each model. Score on each bus is a weighted average
    over bus score on respective model.
    Final score is equal to maximum result from among each of aggregated buses' results.
    """
    detection_results = detection_result.DetectionResult.multiple_models_result(
        dict(autoencoder_bus_results, **isolationforest_bus_results))

    ae_k1_result = autoencoder_bus_results['autoencoder']['k1_result']
    if_k1_result = isolationforest_bus_results['isolationforest']['k1_result']

    # because all values are equal and anomaly accuracy if and only if score is greater than threshold
    assert not detection_results.anomaly
    assert not detection_results.k1_result.anomaly

    def compute_weighted_average(a_w, i_w, score_a, score_i):
        return ((score_a * a_w) + (score_i * i_w)) / (a_w + i_w)

    # isclose is required due to float precision
    assert isclose(detection_results.normalized_score,
                   compute_weighted_average(aggregation_weights['autoencoder_weight'],
                                            aggregation_weights[
                                                'isolationforest_weight'],
                                            ae_k1_result.normalized_score,
                                            if_k1_result.normalized_score), rel_tol=1e-06)

    assert isclose(detection_results.score, compute_weighted_average(aggregation_weights['autoencoder_weight'],
                                                                     aggregation_weights['isolationforest_weight'],
                                                                     ae_k1_result.not_normalized_score,
                                                                     if_k1_result.not_normalized_score), rel_tol=1e-06)

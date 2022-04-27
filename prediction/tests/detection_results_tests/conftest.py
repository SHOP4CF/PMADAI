import pytest
from importlib import reload

from src.detection_results import detection_result, bus_detection_results


@pytest.fixture
def bus_results_dict_with_highest_score_on_first_bus(request):
    val = request.param
    k1_result = bus_detection_results.BusDetectionResult(
        not_normalized_score=val['not_normalized_score'],
        normalized_score=val['normalized_score'],
        threshold=val['threshold'],
        normalized_threshold=val['normalized_threshold']
    )
    k_result = bus_detection_results.BusDetectionResult(
        not_normalized_score=val['not_normalized_score'] - val['constant_subtracted'],
        normalized_score=val['normalized_score'] - val['constant_subtracted'],
        threshold=val['threshold'] - val['constant_subtracted'],
        normalized_threshold=val['normalized_threshold'] - val['constant_subtracted']
    )

    return {
        'k1_result': k1_result,
        'k2_result': k_result,
        'k3_result': k_result,
        'k4_result': k_result
    }


@pytest.fixture(params=[3.19, 0.78])
def autoencoder_bus_results(request):
    # Doesn't matter if score is normalized or not. In this case we only care about aggregation over fields -
    # if aggregate will be made properly, other numbers also will be aggregate correctly.
    result = bus_detection_results.BusDetectionResult(
        not_normalized_score=request.param,
        normalized_score=request.param,
        threshold=request.param,
        normalized_threshold=request.param
    )

    return {
        'autoencoder': {
            'k1_result': result,
            'k2_result': result,
            'k3_result': result,
            'k4_result': result
        }
    }


@pytest.fixture(params=[2.56, 0.47])
def isolationforest_bus_results(request):
    # Doesn't matter if score is normalized or not. In this case we only care about aggregation over fields -
    # if aggregate will be made properly, other numbers also will be aggregate correctly.
    result = bus_detection_results.BusDetectionResult(
        not_normalized_score=request.param,
        normalized_score=request.param,
        threshold=request.param,
        normalized_threshold=request.param
    )

    return {
        'isolationforest': {
            'k1_result': result,
            'k2_result': result,
            'k3_result': result,
            'k4_result': result
        }
    }


@pytest.fixture
def aggregation_weights(request, setup_config_weights):
    a_w, i_w = request.param
    setup_config_weights(a_w, i_w)

    reload(detection_result)

    return {
        'autoencoder_weight': a_w,
        'isolationforest_weight': i_w
    }

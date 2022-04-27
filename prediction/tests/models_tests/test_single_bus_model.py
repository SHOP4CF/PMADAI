import pytest
import numpy as np

from src.models.models_instances.autoencoder import Autoencoder


def empty_function(self):
    pass


def get_autoencoder(model_configuration):
    Autoencoder.load_model = empty_function
    Autoencoder.load_encoder_if_required = empty_function
    autoencoder = Autoencoder(model_configuration)
    return autoencoder


def test_reconstruction_score(model_configuration):
    autoencoder_model = get_autoencoder(model_configuration)
    true_value = np.array([[3, 2, 1]])
    predicted_value = np.array(([[3, 1, 2]]))

    rec_score = autoencoder_model.reconstruction_score(true_value, predicted_value)
    assert rec_score == 2 / 3


def test_is_valid():
    assert not Autoencoder.is_valid(np.array([None]))
    assert not Autoencoder.is_valid(np.array([[[np.inf]]]))
    # assert not Autoencoder.is_valid(np.array([[np.log(0)]]))
    assert not Autoencoder.is_valid(np.array([np.nan]))
    assert Autoencoder.is_valid(np.array([1.0, 2.0]))


def test_exdend_dimension():
    assert Autoencoder.extend_dimension(np.array([1.0, 1.0])).shape == (1, 2)
    assert Autoencoder.extend_dimension(np.array([[1.0, 1.0]])).shape == (1, 2)


@pytest.mark.parametrize('model_configuration', [
    ({
        'scaler_var': 1.0,
        'scaler_mean': 0.0
    })
], indirect=True)
def test_leave_same_after_scaling(model_configuration):
    data = np.array([1.0, 2.0, 3.0, 4.0])
    autoencoder_model = get_autoencoder(model_configuration)
    assert (autoencoder_model.scale_input_data(data) == data).all()


@pytest.mark.parametrize('model_configuration', [
    ({
        'scaler_var': 4.0,
        'scaler_mean': 1.0
    })
], indirect=True)
def test_scale_input_data(model_configuration):
    data = np.array([1.0, 2.0, 3.0, 4.0])
    autoencoder_model = get_autoencoder(model_configuration)
    expected_result = np.array([0.0, 0.5, 1.0, 1.5])
    assert (autoencoder_model.scale_input_data(data) == expected_result).all()


@pytest.mark.parametrize('model_configuration', [
    ({
        'std_multiplication': None,
    })
], indirect=True)
def test_normalize_output_score_without_std_multiplication(model_configuration):
    score = 10.0
    autoencoder_model = get_autoencoder(model_configuration)
    assert autoencoder_model.normalize_output_score(score) == score


@pytest.mark.parametrize('model_configuration', [
    ({
        'std_multiplication': 1.0,
        'result_upper_bound': 11.0,
        'result_mean': 0.0,
        'result_var': 1.0
    }),
    ({
        'std_multiplication': 2.0,
        'result_upper_bound': 11.0,
        'result_mean': 0.0,
        'result_var': 1.0
    })
], indirect=True)
def test_normalize_output_score_without_upper_bound(model_configuration):
    score = 10.0
    autoencoder_model = get_autoencoder(model_configuration)
    assert autoencoder_model.normalize_output_score(score) == (
            1 / (1 + np.power(np.e, -score / model_configuration.std_multiplication)))


@pytest.mark.parametrize('model_configuration', [
    ({
        'std_multiplication': 1.0,
        'result_upper_bound': 5.0,
        'result_mean': 0.0,
        'result_var': 1.0
    })
], indirect=True)
def test_normalize_output_score_with_upper_bound(model_configuration):
    score = 10.0
    autoencoder_model = get_autoencoder(model_configuration)
    assert autoencoder_model.normalize_output_score(score) == (
            1 / (1 + np.power(np.e, -model_configuration.result_upper_bound / model_configuration.std_multiplication)))

import pytest

from src.domain.prediction_data import SingleBusPredictionData


@pytest.mark.preparation
def test_correct_yielding(nested_data, cg33_2000_correct_data):
    assert (nested_data.painting_process_data == cg33_2000_correct_data).all()
    for single_bus_data, real_data in zip(nested_data, cg33_2000_correct_data):
        # Checking if during iterating over nested data, data are stored in SingleBusPredictionData.
        assert isinstance(single_bus_data, SingleBusPredictionData)
        # Checking correctness of building encoding pair string.
        assert single_bus_data.encoding_pair == 'CG332000'
        # Checking if nested data yielding correct data obtained from processed batch.
        assert (single_bus_data.painting_process_data == real_data).all()

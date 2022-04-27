import json
import os
import pytest
from functools import cached_property


class TestPrediction:
    CG33_2000_not_anomaly = os.path.join('tests', 'test_data', 'CG33_2000_correct_all_buses')
    CG33_2000_anomaly = os.path.join('tests', 'test_data', 'CG33_2000_incorrect_bus')

    CG43_2000_not_anomaly = os.path.join('tests', 'test_data', 'CG43_2000_correct_all_buses')
    CG43_2000_anomaly = os.path.join('tests', 'test_data', 'CG43_2000_incorrect_bus')

    GENERAL_not_anomaly = os.path.join('tests', 'test_data', 'general_correct_all_buses')
    GENERAL_anomaly = os.path.join('tests', 'test_data', 'general_incorrect_bus')

    def load_data(self, path):
        with open(path, 'r') as j:
            data = json.loads(j.read())
        return data

    @cached_property
    def not_anomalous_waveforms(self):
        cg33_2000 = self.load_data(TestPrediction.CG33_2000_not_anomaly)
        cg43_2000 = self.load_data(TestPrediction.CG43_2000_not_anomaly)
        general_2000 = self.load_data(TestPrediction.GENERAL_not_anomaly)
        return [cg33_2000, cg43_2000, general_2000]

    @cached_property
    def anomalous_waveforms(self):
        cg33_2000 = self.load_data(TestPrediction.CG33_2000_anomaly)
        cg43_2000 = self.load_data(TestPrediction.CG43_2000_anomaly)
        general_2000 = self.load_data(TestPrediction.GENERAL_anomaly)
        return [cg33_2000, cg43_2000, general_2000]

    @pytest.mark.single_model
    def test_single_type_model_correct_paintings(self, single_models_handler):
        for data in self.not_anomalous_waveforms:
            model_result = single_models_handler(data['payload'])
            assert not model_result.anomaly
            assert model_result.normalized_score <= 1.0
            for bus in ['k1_result', 'k2_result', 'k3_result', 'k4_result']:
                assert getattr(model_result, bus).normalized_score <= 1

    @pytest.mark.single_model
    def test_single_type_model_incorrect_paintings(self, single_models_handler):
        for data in self.anomalous_waveforms:
            model_result = single_models_handler(data['payload'])
            assert model_result.anomaly
            assert model_result.k3_result.anomaly
            assert model_result.normalized_score <= 1.0
            for bus in ['k1_result', 'k2_result', 'k3_result', 'k4_result']:
                assert getattr(model_result, bus).normalized_score <= 1

    @pytest.mark.multiple_models
    def test_multiple_types_models_correct_paintings(self, multiple_models_handler):
        for data in self.not_anomalous_waveforms:
            model_result = multiple_models_handler(data['payload'])
            assert not model_result.anomaly
            assert model_result.normalized_score <= 1.0
            for bus in ['k1_result', 'k2_result', 'k3_result', 'k4_result']:
                assert getattr(model_result, bus).normalized_score <= 1

    @pytest.mark.multiple_models
    def test_multiple_types_models_incorrect_paintings(self, multiple_models_handler):
        for data in self.anomalous_waveforms:
            model_result = multiple_models_handler(data['payload'])
            assert model_result.anomaly
            assert model_result.k3_result.anomaly
            assert model_result.normalized_score <= 1.0
            for bus in ['k1_result', 'k2_result', 'k3_result', 'k4_result']:
                assert getattr(model_result, bus).normalized_score <= 1

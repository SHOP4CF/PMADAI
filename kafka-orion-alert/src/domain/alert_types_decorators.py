from typing import Union, Dict


def basic_alert_decorator(basic_alert):
    """
    Decorator that adds a field to the alert type class informing about the url under which the anomaly can be analyzed.
    """

    @property
    def url(self):
        return f"http://localhost:8080/explore?car-body-id={self.metadata['carBodyId']}"

    basic_alert.url = url
    return basic_alert


def incorrect_painting_process_decorator(incorrect_painting_process):
    """
    Decorator which adds, to the class of incorrect painting process, a field containing an exact description of the alert.
    Description contains information about name and source of alert, string with buses considered as anomalous
    and additional information understood as metadata of the painting process.
    """

    @property
    def description(self):
        additional_information = ' '.join(f"{key}: {val}," for key, val in self.metadata.items())
        return f"Incorrect painting precess during KTL. " \
               f"Alert source: {self.source} " \
               f"{self._get_models_results()}" \
               f"{self._get_human_result_if_required()}" \
               f"Additional information: {additional_information} "\
               f"URL in PMADAI component: {self.url}"

    def _get_human_result_if_required(self):
        """
        This function convert human report to string with buses considered as anomalous.
        """
        result = ''
        if self.human_verified:
            anomalous_buses = get_anomalous_buses(self.human_result)
            if any_anomalous_bus(anomalous_buses):
                result = f"Human result with anomalous buses: {anomalous_buses.rstrip(', ')}. "
            else:
                result = f"Human reports no anomalous waveforms. "

        return result

    def _get_models_results(self):
        """
        This function convert model's prediction to string with buses considered as anomalous.
        """
        anomalous_buses = get_anomalous_buses(self.prediction_result)
        if any_anomalous_bus(anomalous_buses):
            return f"Anomalous buses: {anomalous_buses.rstrip(', ')}. "
        else:
            return f"Model did not report any anomalies. "

    def get_anomalous_buses(anomalous_buses_dict: Dict) -> str:
        anomalous_buses = ''
        for bus in ['K1', 'K2', 'K3', 'K4']:
            if get_value(anomalous_buses_dict[bus]):
                anomalous_buses += f"{bus}, "
        return anomalous_buses

    def get_value(bus: Union[str, Dict]) -> str:
        if isinstance(bus, dict):
            return bus['anomaly']
        else:
            return bus

    def any_anomalous_bus(anomalous_buses: str) -> bool:
        return anomalous_buses != ''

    incorrect_painting_process._get_models_results = _get_models_results
    incorrect_painting_process._get_human_result_if_required = _get_human_result_if_required
    incorrect_painting_process.description = description
    return incorrect_painting_process


def incorrect_painting_data_decorator(incorrect_painting_data):
    """
    Decorator which adds, to the incorrect painting data class, a field containing an exact description of the alert.
    Description contains information about name and source of alert and additional information understood as metadata of the painting process.
    """

    @property
    def description(self):
        additional_information = ' '.join(f"{key}: {val}," for key, val in self.metadata.items())
        return f"Incorrect painting data." \
               f"Alert source: {self.source} " \
               f"Additional information: {additional_information} " \
               f"URL in PMADAI component: {self.url}"

    incorrect_painting_data.description = description
    return incorrect_painting_data


def unhandled_alert_decorator(unhandled_alert):
    """
    Decorator which adds, to the class with unhandled alert, a field  containing an exact description of the alert.
    """

    @property
    def description(self):
        return "Unknown alert."

    unhandled_alert.description = description
    return unhandled_alert

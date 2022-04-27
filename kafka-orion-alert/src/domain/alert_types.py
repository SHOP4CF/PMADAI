from typing import Dict
from abc import abstractmethod
import src.domain.alert_types_decorators as decorator


@decorator.basic_alert_decorator
class BasicAlert:
    """
    This class is contains information about alert.
    It retrieves data from raw alert and saving them in specific structured way.
    The subclass should implement 'to_dict' method.

    Attributes
    ----------
    source : str
        Source that triggered the alert.
    metadata : Dict
        Metadata about painting process.
    date_issued : str
        Value that indicates the date when the anomaly occurred. Date format: %Y-%m-%dT%H:%M:%S.%fZ
    date_modified : str
        Value that indicates the date when the modification of data occurred.
    human_verified : bool
        Value identifying whether the human has verified the data.
    """

    def __init__(self, alert_data: Dict):
        """
        Parameters
        ----------
        alert_data : Dict
            Raw alert retrieved from the kafka topic on the basis of which detailed information is extracted.
        """
        self.source = alert_data['source']
        self.metadata = alert_data['metadata']
        self.date_issued = alert_data['date_issued']
        self.human_verified = alert_data['human_verified'] if 'human_verified' in alert_data.keys() else False
        self.date_modified = alert_data['date_modified'] if 'date_modified' in alert_data.keys() else self.date_issued

    @abstractmethod
    def to_dict(self):
        """
        Method which return dictionary with instance variable names and values.
        """
        pass

    def __str__(self):
        return str(self.to_dict())


@decorator.incorrect_painting_process_decorator
class IncorrectPaintingProcess(BasicAlert):
    """
    Class represents an alert resulting from an incorrect KTL painting process.

    Attributes
    ----------
    name : str
        Name representing the circumstances of generating the alert.
    prediction_result : Dict
        Results of models prediction which cause the alert.
    human_result : Dict
        Results of human report with anomalous buses.
    """

    def __init__(self, alert_data: dict):
        self.name = 'incorrectPaintingProcessInKTL'
        self.prediction_result = alert_data['prediction_result']
        self.human_result = alert_data['human_result']
        super(IncorrectPaintingProcess, self).__init__(
            alert_data=alert_data
        )

    def to_dict(self):
        return {
            'name': self.name,
            'source': self.source,
            'prediction_result': self.prediction_result,
            'human_result': self.human_result,
            'metadata': self.metadata,
            'date_issued': self.date_issued,
            'date_modified': self.date_modified,
            'human_verified': str(self.human_verified)
        }


@decorator.incorrect_painting_data_decorator
class IncorrectPaintingData(BasicAlert):
    """
    Class represents an alert resulting from an incorrect painting data.

    Attributes
    ----------
    name : str
        Name representing the circumstances of generating the alert.
    """

    def __init__(self, alert_data: dict):
        self.name = 'incorrectPaintingData'
        super(IncorrectPaintingData, self).__init__(
            alert_data=alert_data
        )

    def to_dict(self):
        return {
            'name': self.name,
            'source': self.source,
            'metadata': self.metadata,
            'date_issued': self.date_issued,
            'date_modified': self.date_modified,
            'human_verified': str(self.human_verified)
        }


@decorator.unhandled_alert_decorator
class UnhandledAlert(BasicAlert):
    """
    Class represents an alert which was received but is unhandled/unknown.

    Attributes
    ----------
    name : str
        Name representing the circumstances of generating the alert.
    """

    def __init__(self):
        self.name = 'unhandledAlert'
        super(UnhandledAlert, self).__init__(
            alert_data={
                'source': 'Unhandled',
                'metadata': None,
                'date_issued': None,
                'date_modified': None,
                'human_verified': False
            }
        )

    def to_dict(self):
        return {
            'name': self.name,
            'source': self.source,
            'metadata': self.metadata,
            'date_issued': self.date_issued,
            'date_modified': self.date_modified,
            'human_verified': str(self.human_verified)
        }

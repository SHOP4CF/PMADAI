import logging
from typing import Optional, List, Dict
from datetime import datetime


class PaintingPrediction:
    """
    This class is responsible for storing painting prediction data. It stores fields containing information
    about the entire process, starting from processing and ending with the results
    of prediction and information about possible confirmation by an expert.
    """

    def __init__(self,
                 id: Optional[int],
                 prediction_result: Dict,
                 human_result: Dict,
                 problematic_painting: bool,
                 preprocessing_status: str,
                 time_of_event: str,
                 in_out: str,
                 car_body_id: str,
                 car_body_type: str,
                 voltage_program_type: str,
                 skid_id: int,
                 pendulum_id: int,
                 histograms: List[List],
                 tsfresh_features: List[List],
                 custom_features: List[List],
                 interpolation_features: List[List],
                 raw_data: Dict,
                 human_verified: bool,
                 date_modified: str):
        self.id = id

        # Prediction result
        self.prediction_result = prediction_result
        self.human_result = human_result
        self.problematic_painting = problematic_painting

        # Preprocessing result
        # Preprocessing result: status
        self.preprocessing_status = preprocessing_status

        # Preprocessing result: payload (metadata)
        self.time_of_event = time_of_event
        self.in_out = in_out
        self.car_body_id = car_body_id
        self.car_body_type = car_body_type
        self.voltage_program_type = voltage_program_type
        self.skid_id = skid_id
        self.pendulum_id = pendulum_id

        # Preprocessing result: payload (features)
        self.histograms = histograms
        self.tsfresh_features = tsfresh_features
        self.custom_features = custom_features
        self.interpolation_features = interpolation_features

        # Preprocessing result: raw data
        self.raw_data = raw_data

        self.human_verified = human_verified

        self.date_modified = date_modified

    @classmethod
    def from_painting_prediction(cls, painting_prediction_json: dict, id: Optional[int] = None):
        """
        This method is creating PaintingPrediction instance based on data derived from prediction module.
        """
        logging.debug(f"Creating PaintingPrediction object from json: {painting_prediction_json}")
        logging.debug(f"ID: {id}")
        time_of_event = datetime.fromisoformat(
            painting_prediction_json['preprocessingResult']['payload']['metadata']['timeOfEvent']).strftime(
            "%Y-%m-%d %H:%M:%S")
        date_modified = datetime.fromisoformat(painting_prediction_json['dateModified']).strftime("%Y-%m-%d %H:%M:%S")
        return cls(id=id,
                   prediction_result=painting_prediction_json['predictionResult'],
                   human_result=painting_prediction_json['humanResult'],
                   problematic_painting=painting_prediction_json['problematicPainting'],
                   preprocessing_status=painting_prediction_json['preprocessingResult']['status'],
                   time_of_event=time_of_event,
                   in_out=painting_prediction_json['preprocessingResult']['payload']['metadata']['inOut'],
                   car_body_id=painting_prediction_json['preprocessingResult']['payload']['metadata']['carBodyId'],
                   car_body_type=painting_prediction_json['preprocessingResult']['payload']['metadata']['carBodyType'],
                   voltage_program_type=painting_prediction_json['preprocessingResult']['payload']['metadata'][
                       'voltageProgramType'],
                   skid_id=painting_prediction_json['preprocessingResult']['payload']['metadata']['skidId'],
                   pendulum_id=painting_prediction_json['preprocessingResult']['payload']['metadata']['pendulumId'],
                   histograms=painting_prediction_json['preprocessingResult']['payload']['histograms'],
                   tsfresh_features=painting_prediction_json['preprocessingResult']['payload']['tsfreshFeatures'],
                   custom_features=painting_prediction_json['preprocessingResult']['payload']['customFeatures'],
                   interpolation_features=painting_prediction_json['preprocessingResult']['payload'][
                       'interpolationFeatures'],
                   raw_data=painting_prediction_json['preprocessingResult']['rawData'],
                   human_verified=painting_prediction_json['humanVerified'],
                   date_modified=date_modified,
                   )

    def to_dict(self) -> dict:
        json_formatted = {
            "predictionResult": self.prediction_result,
            "humanResult": self.human_result,
            "problematicPainting": self.problematic_painting,
            "humanVerified": self.human_verified,
            "dateModified": self.date_modified,
            "preprocessingResult": {
                "status": self.preprocessing_status,
                "payload": {
                    "metadata": {
                        'timeOfEvent': self.time_of_event,
                        'inOut': self.in_out,
                        'carBodyId': self.car_body_id,
                        'carBodyType': self.car_body_type,
                        'voltageProgramType': self.voltage_program_type,
                        'skidId': self.skid_id,
                        'pendulumId': self.pendulum_id
                    },
                    "histograms": self.histograms,
                    "tsfreshFeatures": self.tsfresh_features,
                    "customFeatures": self.custom_features,
                    "interpolationFeatures": self.interpolation_features
                },
                'rawData': self.raw_data
            }
        }

        if self.id:
            json_formatted['id'] = self.id

        return json_formatted

    def __str__(self):
        return f"PaintingPrediction: {self.to_dict()}"

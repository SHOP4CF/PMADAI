from typing import Mapping

import numpy as np

from src.domain.metadata import Metadata
from src.domain.preprocessing_result import PreprocessingResult, PreprocessingStatus, PreprocessingPayload, RawData
from src.domain.waveform import Waveform
from src.preprocessors.preprocessor import Preprocessor
from datetime import datetime
import logging


class TimeBasedPreprocessor(Preprocessor):
    """
    Preprocessor based on time. Extracts shapes from buses in predefined timeframes.
    """
    def __init__(self):
        self.shifts = {
            "K1": (np.timedelta64(5, 's'), np.timedelta64(2 * 60 + 46, 's')),
            "K2": (np.timedelta64(2 * 60 + 29, 's'), np.timedelta64(5 * 60 + 5, 's')),
            "K3": (np.timedelta64(4 * 60 + 46, 's'), np.timedelta64(7 * 60 + 30, 's')),
            "K4": (np.timedelta64(6 * 60 + 52, 's'), np.timedelta64(9 * 60 + 18, 's'))
        }
        self.bus_to_trend_name = {
            "K1": "current_on_busbar_1",
            "K2": "current_on_busbar_2",
            "K3": "current_on_busbar_3",
            "K4": "current_on_busbar_4"
        }
        self.current_trends_measurement_name = "CurrentTrends"

    def preprocess(self, metadata: Metadata, trends: Mapping) -> PreprocessingResult:
        # Get KTL entry time
        ktl_entry_time = metadata.time_of_event

        # Convert to numpy datetime 64
        dt = datetime.strptime(ktl_entry_time, "%Y-%m-%d %H:%M:%S.%f")
        ktl_entry_time_dt64 = np.datetime64(dt)

        # Get current trends
        current_trends_dict = trends[self.current_trends_measurement_name]

        # Extract waveforms
        logging.info("Waveform extraction.")
        bus_to_extracted_waveform = self.extract_waveforms(current_trends_dict, ktl_entry_time_dt64)

        waveforms = bus_to_extracted_waveform.values()
        raw_data = RawData(waveforms=bus_to_extracted_waveform)

        if any([len(w.values) == 0 for w in waveforms]):
            # Nothing was extracted on one of the buses -> GAP IN READINGS!
            logging.debug(f"Nothing was extracted, gap in readings.")
            preprocessing_status = PreprocessingStatus.GAP_IN_READINGS

            return PreprocessingResult(preprocessing_status=preprocessing_status,
                                       payload=PreprocessingPayload(metadata=metadata),
                                       raw_data=raw_data)
        else:
            preprocessing_status = PreprocessingStatus.CORRECT

            # Construct payload
            logging.info("Payload construction.")
            payload = self.construct_payload(metadata, bus_to_extracted_waveform)

            logging.debug(f"Payload: {payload.to_dict()}")

            return PreprocessingResult(preprocessing_status=preprocessing_status,
                                       payload=payload,
                                       raw_data=raw_data)

    def extract_waveforms(self, current_trends_dict, ktl_entry_time) -> Mapping[str, Waveform]:
        result = {}
        for bus, trend_name in self.bus_to_trend_name.items():
            cutoff_start = ktl_entry_time + self.shifts[bus][0]
            cutoff_end = ktl_entry_time + self.shifts[bus][1]

            sub_df = current_trends_dict[trend_name].loc[cutoff_start:cutoff_end]
            waveform = Waveform(bus, sub_df['value'].values, sub_df.index.values)

            result[bus] = waveform
        return result

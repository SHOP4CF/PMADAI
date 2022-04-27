import abc
import pandas as pd
from typing import Mapping


class TimeSeriesRepository:
    @abc.abstractmethod
    def get_trends_values(self, time_from, time_to) -> Mapping[str, pd.DataFrame]:
        pass

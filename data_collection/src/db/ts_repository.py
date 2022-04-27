import abc


class TimeSeriesRepository:
    @abc.abstractmethod
    def save_measurement(self, measurement, trend_name, timestamp, value):
        pass

import abc


class RelationalRepository:
    @abc.abstractmethod
    def insert_alert(self, alert):
        pass

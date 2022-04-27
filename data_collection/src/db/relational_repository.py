import abc

from src.domain.metadata import Metadata


class RelationalRepository:
    @abc.abstractmethod
    def insert_metadata_row(self, metadata: Metadata):
        pass

    @abc.abstractmethod
    def insert_smt_entry(self, smt_entry):
        pass


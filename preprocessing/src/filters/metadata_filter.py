import abc

from src.domain.metadata import Metadata
from src.domain.preprocessing_result import PreprocessingStatus


class MetadataFilter:
    """
    Main purpose of the class is to apply it as a filter before preprocessing.
    """
    def __init__(self, status: PreprocessingStatus):
        self.status: PreprocessingStatus = status

    @abc.abstractmethod
    def apply(self, metadata: Metadata) -> bool:
        pass
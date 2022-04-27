from src.domain.metadata import Metadata
from src.domain.preprocessing_result import PreprocessingStatus
from src.filters.metadata_filter import MetadataFilter


class CageFilter(MetadataFilter):
    def __init__(self):
        super().__init__(PreprocessingStatus.CAGE)

    def apply(self, metadata: Metadata) -> bool:
        if metadata.voltage_program_type == 'TC00' and metadata.car_body_type == '0000':
            return True
        return False
from enum import Enum


class PreprocessingStatus(Enum):
    """
    The processing ends with one of the 4 statuses:\n
    - CORRECT -> The preprocessing  was completed without problems
    - CAGE -> Some of the data considers painting of so called 'cages'. Those shapes should be treated separately because they are inherently different from rest of the data.
    - GAP_IN_READINGS -> There was a gap in readings on any of the buses. There is no data to apply preprocessing to.
    - BAD_EXTRACTION -> The preprocessing could not be completed from unpredictable reasons.
    """
    CORRECT = "CORRECT"
    CAGE = "CAGE"
    GAP_IN_READINGS = "GAP_IN_READINGS"
    BAD_EXTRACTION = "BAD_EXTRACTION"

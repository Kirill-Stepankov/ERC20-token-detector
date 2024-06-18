from enum import Enum


class ProcessingStatus(str, Enum):
    WAITS_PROCESSING = "Waits processing"
    PROCESSING = "Processing"
    PROCESSED = "Processed"
    FAILED = "Failed"

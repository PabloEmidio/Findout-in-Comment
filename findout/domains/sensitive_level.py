from enum import Enum, unique


@unique
class SensitiveLevelsEnum(Enum):
    HIGH = 'High'
    LOW = 'Low'
    MEDIUM = 'Medium'
    OPTIONAL = 'Optional'

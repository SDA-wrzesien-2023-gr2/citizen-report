from enum import Enum


class Department(Enum):
    APP = 'Applicant'
    SYS = 'System supervisor'
    RBR = 'Roads and bridges'
    SWS = 'Sewer and waterworks'
    POW = 'Power supply'
    GAS = 'Gasworks'
    TEL = 'Telecommunication'
    GAR = 'Garbage disposal'
    CTR = 'City transport'
    HTH = 'Healthcare'
    EDU = 'Education'
    SAF = 'Public safety'

    @classmethod
    def choices(cls):
        return [(item.name, item.value) for item in cls]


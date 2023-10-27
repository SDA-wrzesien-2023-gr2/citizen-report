from django.db import models


class Category(models.TextChoices):
    ROADS_AND_BRIDGES = 'RBR', 'Roads and bridges'
    SEWER_AND_WATERWORKS = 'SWS', 'Sewer and waterworks'
    POWER_SUPPLY = 'POW', 'Power supply'
    GASWORKS = 'GAS', 'Gasworks'
    TELECOMMUNICATION = 'TEL', 'Telecommunication'
    GARBAGE_DISPOSAL = 'GAR', 'Garbage disposal'
    CITY_TRANSPORT = 'CTR', 'City transport'
    HEALTHCARE = 'HTH', 'Healthcare'
    EDUCATION = 'EDU', 'Education'
    PUBLIC_SAFETY = 'SAF', 'Public safety'


class Status(models.TextChoices):
    PENDING = 'PN', 'Pending'
    CHECKING = 'CH', 'Checking'
    REJECTED = 'RJ', 'Rejected'
    APPROVED = 'AP', 'Approved'

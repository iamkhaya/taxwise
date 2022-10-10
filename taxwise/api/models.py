# coding: utf-8
from django.db import models


class Tarriff(models.Model):
    """tarriff model"""

    heading = models.CharField(max_length=30)
    commodity_code = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    statistical_unit = models.CharField(max_length=30)
    general_rate_of_duty = models.CharField(max_length=30)
    mtf_rate_of_duty = models.CharField(max_length=30)

class ChapterSection(models.Model):
    """chapter section model"""

    chapter = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    
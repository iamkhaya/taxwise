# coding: utf-8
from django.db import models


class Tarriff(models.Model):
    """tarriff model"""

    heading = models.CharField(max_length=100, null=True)
    commodity_code = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    statistical_unit = models.CharField(max_length=30, null=True)
    general_rate_of_duty = models.CharField(max_length=30, null=True)
    mtf_rate_of_duty = models.CharField(max_length=30, null=True)


class ChapterSection(models.Model):
    """chapter section model"""

    chapter = models.CharField(max_length=100, null=True)
    section = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)

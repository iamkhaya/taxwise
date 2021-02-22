from __future__ import unicode_literals

from django.db import models

class Tarriff(models.Model):
  chapter = models.IntegerField()
  heading = models.DecimalField(max_digits=10, decimal_places=2)
  sub_heading =  models.DecimalField(max_digits=10, decimal_places=2)
  sub_sub_heading =  models.DecimalField(max_digits=10, decimal_places=2)
  cd =  models.IntegerField()
  description = models.TextField()
  statistical_unit = models.TextField()
  general_rate_of_duty = models.DecimalField(max_digits=10, decimal_places=2)
  eu_rate_of_duty =  models.DecimalField(max_digits=10, decimal_places=2)
  efta_rate_of_duty =  models.DecimalField(max_digits=10, decimal_places=2)
  sadc_rate_of_duty =  models.DecimalField(max_digits=10, decimal_places=2)
  mercosur_rate_of_duty =  models.DecimalField(max_digits=10, decimal_places=2)


class Headings(models.Model):
  heading = models.DecimalField(max_digits=10, decimal_places=2)
  description =  models.TextField()


class Chapter(models.Model):
  chapter =  models.IntegerField()
  note =  models.TextField()
  additional_note =  models.TextField()


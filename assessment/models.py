from django.db import models
from account.models import Expert
from assessment.validator import *


class Quality(models.Model):
    quality = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.quality

    # TODO: реализовать рассчёт коэффициента
    def math_func(self):
        assessments = self.assessment_set().all()  # Возвращает QuerySet c объектами Assessment


class Assessment(models.Model):
    quality = models.ForeignKey('Quality')
    expert = models.ForeignKey('account.Expert')
    point = models.PositiveSmallIntegerField(validators=[validate_point])

    class Meta:
        unique_together = ("quality", "expert")

from django.db import models
from django.conf import settings
from assessment.validator import *

CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE', 'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']


class Person(models.Model):

    last_name = models.CharField(max_length=30, validators=[validate_name])
    first_name = models.CharField(max_length=30, validators=[validate_name])
    patronymic = models.CharField(max_length=30, validators=[validate_name])
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "%s %s.%s." % (self.last_name, self.first_name[0], self.patronymic[0])

    class Meta:
        abstract = True


class Expert(Person):

    profession = models.CharField(max_length=30, validators=[validate_profession])
    position = models.CharField(max_length=30, validators=[validate_profession])
    professional_experience = models.PositiveSmallIntegerField(validators=[validate_experience])
    driver_license = models.CharField(max_length=30,
                                      blank=True,
                                      choices=((cat, cat) for cat in CATEGORIES))
    driving_experience = models.IntegerField(blank=True, validators=[validate_experience])

    def save(self, *args, **kwargs):
        if not self.driver_license:
            self.driving_experience = False
        super(Expert, self).save(*args, **kwargs)


class Quality(models.Model):

    quality = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.quality


class Assessment(models.Model):

    quality = models.ForeignKey('Quality')
    expert = models.ForeignKey('Expert')
    point = models.PositiveSmallIntegerField(validators=[validate_point])

    class Meta:
        unique_together = ("quality", "expert")

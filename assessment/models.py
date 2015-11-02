from django.db import models

CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE', 'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']


class Person(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    def __str__(self):
        return self.last_name

    class Meta:
        abstract = True


class Driver(Person):
    pass


class Expert(Person):
    profession = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    professional_experience = models.IntegerField()
    driver_license = models.CharField(max_length=30,
                                      blank=True)
    driving_experience = models.IntegerField()


class Quality(models.Model):
    quality = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.quality


class Assessment(models.Model):
    quality = models.ForeignKey('Quality')
    expert = models.ForeignKey('Expert')
    driver = models.ForeignKey('Driver')
    point = models.IntegerField()

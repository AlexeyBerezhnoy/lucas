from django.db import models

CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE',
              'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']


class Person(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    def __str__(self):
        return "%s %s.%s", % (self.last_name,
                              self.first_name[1],
                              self.patronymic[1])

    class Meta:
        abstract = True


# Этот класс ещё нужно доделать после обсуждения с зказчиком
class Expert(Person):
    profession = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    professional_experience = models.DurationField()
    driver_license = models.CharField(max_length=30,
                                      choises=((x, x) for x in CATEGORIES)
                                      blank=True)
    driving_experience = models.DurationField()


class Quality(models.Model):
    quality = models.CharField(max_length=30)
    description = models.TextField()
    point = models.IntegerField()

    def __str__(self):
        return self.quality


class Assessment(models.Model):
    expert = models.ForeinKey('Expert')
    quality = models.ManyToManyField('Quality')


class Driver(Person):
    assessment = models.ManyToManyField('Assessment')

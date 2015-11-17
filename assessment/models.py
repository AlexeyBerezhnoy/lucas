from django.db import models


class Person(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    def __str__(self):
        return "%s %s.%s." % (self.last_name, self.first_name[0], self.patronymic[0])

    class Meta:
        abstract = True


class Expert(Person):
    CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE', 'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']
<<<<<<< HEAD

=======
>>>>>>> 13653a1
    profession = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    professional_experience = models.IntegerField()
    driver_license = models.CharField(max_length=30,
<<<<<<< HEAD
                                      blank=True,
                                      choices=((cat, cat) for cat in CATEGORIES))
=======
                                      choices=((x, x) for x in CATEGORIES),
                                      blank=True)
>>>>>>> 13653a1
    driving_experience = models.IntegerField(blank=True)


class Quality(models.Model):
    quality = models.CharField(max_length=60)
    description = models.TextField()

    def get_assessment(self):
        pass

    def __str__(self):
        return self.quality


class Assessment(models.Model):
    quality = models.ForeignKey('Quality')
    expert = models.ForeignKey('Expert')
    point = models.IntegerField()

from django.db import models
import scipy
import scipy.stats
from account.models import Expert
from assessment.math import math_func
from assessment.validator import *

QUALITY_CATEGORY = (("VS", "Свойства зрительного анализаторов"),
                    ("HR", "Свойства слухового анализатора"),
                    ("SM", "Свойства обонятельного анализатора"),
                    ("TM", "Свойства температурного анализатора"),
                    ("TC", "Свойства тактильного анализатора"),
                    ("AT", "Свойства внимания"),
                    ("MM", "Свойства памяти"),
                    ("TN", "Свойства мышления"),
                    ("RT", "Сенсомоторные реакции"),
                    ("VM", "Свойства зрительного, двигательного, вестибулярного, слухового анализаторов"),
                    ("VH", "Свойства зрительного, слухового, кожного, двигательного анализаторов"),
                    ("AI", "Свойства интеллекта"),
                    ("VV", "Свойства зрительного и вестибулярного анализаторов"),
                    ("HN", "Свойства высшей нервной деятельности"),
                    ("EM", "Свойства эмоционально-волевой и мотивационной сфер"))


class Quality(models.Model):
    quality = models.CharField(max_length=60)
    category = models.CharField(max_length=60,
                                choices=QUALITY_CATEGORY)
    description = models.TextField()

    def __str__(self):
        return self.quality

    def average_assessment(self):
        return scipy.average([i.point for i in self.assessment_set.all()])


class Assessment(models.Model):
    quality = models.ForeignKey('Quality')
    expert = models.ForeignKey('account.Expert')
    point = models.IntegerField(validators=[validate_point])

    class Meta:
        unique_together = ("quality", "expert")

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

    def get_category(self):
        for category in QUALITY_CATEGORY:
            if self.category == category[0]:
                return category[1]

    def average_assessment(self):
        table = []
        for e in Expert.objects.all():
            if e.is_expert:
                assessments = []
                mask = []
                for q in Quality.objects.all():
                    try:
                        assessments.append(Assessment.objects.get(expert=e, quality=q).point)
                        mask.append(0)
                    except Exception:
                        assessments.append(0)
                        mask.append(1)
                masked_assessments = scipy.ma.array(assessments, mask=mask)
                table.append(masked_assessments)

        # to range

        if math_func(table):
            return scipy.average([i.point for i in self.assessment_set.all()])
        return -1


class Assessment(models.Model):
    quality = models.ForeignKey('Quality')
    expert = models.ForeignKey('account.Expert')
    point = models.PositiveSmallIntegerField(validators=[validate_point])
    rank = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ("quality", "expert")
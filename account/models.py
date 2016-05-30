from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from account.validator import validate_name, validate_profession, validate_experience

CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE', 'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']


class MyUserManager(BaseUserManager):
    def create_moderator(self, email, last_name, first_name, middle_name):
        # TODO: Сделай email нормальным
        user = self.model(email=email,
                          last_name=last_name,
                          first_name=first_name,
                          middle_name=middle_name)
        user.is_moderator = True
        user.save()
        return user

    def create_expert(self, email, last_name, first_name, middle_name,
                      profession, professional_experience, position,
                      driver_license, driving_experience):
        user = self.model(email=email, last_name=last_name, first_name=first_name, middle_name=middle_name,
                          profession=profession, professional_experience=professional_experience, position=position,
                          driver_license=driver_license, driving_experience=driving_experience)
        user.is_expert = True
        user.save()

    def create_superuser(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.is_moderator = True
        user.save()


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email",
                              unique=True)
    last_name = models.CharField("фамилия",
                                 max_length=30,
                                 validators=[validate_name])
    first_name = models.CharField("имя",
                                  max_length=30,
                                  validators=[validate_name])
    middle_name = models.CharField("отчество",
                                   max_length=30,
                                   validators=[validate_name])

    profession = models.CharField("профессия",
                                  max_length=30,
                                  blank=True,
                                  validators=[validate_profession])
    position = models.CharField("должность",
                                max_length=30,
                                blank=True,
                                validators=[validate_profession])
    professional_experience = models.PositiveSmallIntegerField("опыт работы",
                                                               null=True,
                                                               validators=[validate_experience])
    driver_license = models.CharField("Водительское удостоверение",
                                      max_length=30,
                                      blank=True,
                                      choices=((cat, cat) for cat in CATEGORIES))
    driving_experience = models.IntegerField("опыт работы",
                                             null=True,
                                             validators=[validate_experience])

    is_expert = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return "%s %s. %s." % (self.last_name, self.first_name[0], self.middle_name[0])

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Moderator(MyUser):
    objects = MyUserManager()

    class Meta:
        proxy = True


class Expert(MyUser):
    objects = MyUserManager()

    def save(self, *args, **kwargs):
        """
        Запрещает сохранять экспертом поле
        водительский стаж без наличия прав
        """
        if not self.driver_license:
            self.driving_experience = False
        super(Expert, self).save(*args, **kwargs)

    class Meta:
        proxy = True

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE', 'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']


class MyUserManager(BaseUserManager):

    def invite(self, email):
        user = self.get(email=email)
        password = self.make_random_password(length=4, allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        user.set_password(password)
        user.save()

        # TODO: поправь ссылки, вынеси текст сообщения из модели
        confirm_link = "http://127.0.0.1:8000/account/confirm/{}/{}/".format(email, password)
        subject = "Welcome"
        message = "Здравтствуйте {} {}, пожалуйста подтвердите регистрацию {}".format(user.first_name,
                                                                                      user.middle_name,
                                                                                      confirm_link)
        send_mail(subject, message, 'admin@lucas.com', [email], fail_silently=False)

    def create_moderator(self, email, last_name, first_name, middle_name):
        # TODO: Сделай email нормальным
        user = self.model(email=email,
                          last_name=last_name,
                          first_name=first_name,
                          middle_name=middle_name)
        user.save()
        self.invite(email)
        return user

    def create_expert(self, email, last_name, first_name, middle_name,
                      profession, professional_experience, position,
                      driver_license, driving_experience):

        user = self.model(email=email, last_name=last_name, first_name=first_name, middle_name=middle_name,
                          profession=profession, professional_experience=professional_experience, position=position,
                          driver_license=driver_license, driving_experience=driving_experience)
        self.invite(email)
        user.save()

    def create_superuser(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)

    profession = models.CharField(max_length=30, blank=True)
    position = models.CharField(max_length=30, blank=True)
    professional_experience = models.PositiveSmallIntegerField(null=True)
    driver_license = models.CharField(max_length=30,
                                      blank=True,
                                      choices=((cat, cat) for cat in CATEGORIES))
    driving_experience = models.IntegerField(null=True)

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
        return self.email

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
        if not self.driver_license:
            self.driving_experience = False
        super(Expert, self).save(*args, **kwargs)

    class Meta:
        proxy = True

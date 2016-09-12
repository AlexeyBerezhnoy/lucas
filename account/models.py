from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission
from account.validator import validate_name, validate_profession, validate_experience

CATEGORIES = ['A', 'A1', 'B', 'B1', 'BE', 'C', 'C1', 'CE', 'C1E', 'D', 'D1', 'DE', 'D1E', 'M', 'Tm', 'Tb']


class ModeratorManager(BaseUserManager):
    def create_moderator(self, email, last_name, first_name, middle_name, password):
        user = self.model(email=self.normalize_email(email),
                          last_name=last_name,
                          first_name=first_name,
                          middle_name=middle_name)
        user.is_admin = True
        user.save()
        user.user_permissions.add(Permission.objects.get(codename='manipulate_expert'))
        user.set_password(password)
        user.save()
        return user

    def get_queryset(self):
        return super(BaseUserManager, self).get_queryset().filter(is_admin=True)


class ExpertManager(BaseUserManager):
    def create_expert(self, email, last_name, first_name, middle_name,
                      profession, professional_experience, position,
                      driver_license, driving_experience):
        user = self.model(email=email, last_name=last_name, first_name=first_name, middle_name=middle_name,
                          profession=profession, professional_experience=professional_experience, position=position,
                          driver_license=driver_license, driving_experience=driving_experience)
        user.save()
        return user

    def get_queryset(self):
        return super(BaseUserManager, self).get_queryset().filter(is_expert=True)


class User(AbstractBaseUser, PermissionsMixin):

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
    driving_experience = models.IntegerField("Водительский стаж",
                                             null=True,
                                             validators=[validate_experience])

    is_expert = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = BaseUserManager()

    def __str__(self):
        return self.email

    # TODO: лучше использовать нормальную проверку пермишинов
    def has_perm(self, perm, obj=None):
        p = Permission.objects.get(codename=perm)

        if p not in self.user_permissions.all():
            return False
        return True

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm):
                return False
        return True


class Moderator(User):
    objects = ModeratorManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.email


class Expert(User):
    objects = ExpertManager()

    def save(self, *args, **kwargs):
        """
        Запрещает сохранять экспертом поле
        водительский стаж без наличия прав
        """
        if not self.driver_license:
            self.driving_experience = False

        self.is_expert = True

        super(Expert, self).save(*args, **kwargs)

    class Meta:
        proxy = True
        permissions = (
            ('manipulate_expert', 'Can create, edit, view and remove expert'),
        )

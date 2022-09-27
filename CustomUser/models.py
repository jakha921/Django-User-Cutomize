from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('this is not correct email.')
        if not username:
            raise ValueError('this is not correct username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60)
    email = models.EmailField(max_length=60, verbose_name='email', unique=True)
    date_joined = models.DateTimeField(auto_now=True, verbose_name='date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_mail = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

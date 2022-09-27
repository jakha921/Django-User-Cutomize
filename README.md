# Django User Customization

## Setup repo on your dives

1. run `git clone https://github.com/jakha921/Django-User-Cutomize.git` on you cmd or PowerShell
2. create venv:
   + `python -m venv <venv_name>` for Windows
   + `python3 -m venv <venv_name>` for Linux
3. activate virtual environment
    + `venv/Script/activate` for Windows
    + `venv/bin/activate` for Linux
4. installation all requirement packages for project run command `pip install -r requirement.txt`

>**Note**: <br />
It is important that **before** applying migrations in your app you must add CustomUser into your model. Again, I want to emphasize that **before** you apply your **first** migration you must add your ‘custom models’.
---

## Code description

### Create User Model
```python
models.py


from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.db import models

class CustomUserManager(BaseUserManager):
   """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
   """
    def create_user(self, email, username, password=None):
        """
            Create and save a User with the given email and password.
        """
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
        """
        Create and save a SuperUser with the given email and password.
        """
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
   """Create custom fields for user which we need to see on User"""
    username = models.CharField(max_length=60)
    email = models.EmailField(max_length=60, verbose_name='email', unique=True)
    date_joined = models.DateTimeField(auto_now=True, verbose_name='date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_mail = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)  # add Gorup & Roles

    # USERNAME_FIELD for entering to admin panel required
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS additional fields to fill in  
    REQUIRED_FIELDS = ('username',)

    # Specified that all objects for the class come from the CustomUserManager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
```

### Add to settings path for this customization
```python
settings.py

# exp:  'CustomUser.CustomUser'
AUTH_USER_MODEL = '<app_name>.<abstract_model_name>'
```

### Create Tables

```shell
cmd

# Before that, you should not have more than one migration
python manage.py makemigrations
python manage.py migrate
```

### Admin panel

```python
admin.py


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    readonly_fields = ('date_joined', 'last_login')

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'groups', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        (None, {
            'fields': ('groups', 'user_permissions',)
        }),
        ("Dates", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
```
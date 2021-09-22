import datetime
from typing import Any

from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import JSONField  # type: ignore
from django.db.models import F, Max, Q

class SortableModel(models.Model):
    sort_order = models.IntegerField(editable=False, db_index=True, null=True)

    class Meta:
        abstract = True

    def get_ordering_queryset(self):
        raise NotImplementedError("Unknown ordering queryset")

    def get_max_sort_order(self, qs):
        existing_max = qs.aggregate(Max("sort_order"))
        existing_max = existing_max.get("sort_order__max")
        return existing_max

    def save(self, *args, **kwargs):
        if self.pk is None:
            qs = self.get_ordering_queryset()
            existing_max = self.get_max_sort_order(qs)
            self.sort_order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.sort_order is not None:
            qs = self.get_ordering_queryset()
            qs.filter(sort_order__gt=self.sort_order).update(
                sort_order=F("sort_order") - 1
            )
        super().delete(*args, **kwargs)

from django.contrib.auth.models import AbstractUser

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

class Market(models.Model):
    url = models.CharField(max_length=1024)

class UserManager(BaseUserManager):
    """
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    """


    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a `User` with an email, username and password.
        """
        user = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')


        username = email.split("@")[0]
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()


        return user

class CASUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model, overrided from django.contrib.auth.models.User."""


    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        blank=False,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    full_name = models.CharField(
        'full name',
        max_length=150,
        blank=False
    )

    mobile = models.CharField(
        'mobile number',
        max_length=15,
        unique=True,
        blank=False,
        error_messages={
            'unique': "A user with that mobile number already exists.",
        })

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    markets_owned_by = models.ManyToManyField(Market, related_name='markets_owned_by')
    waiters_owned_by = models.ManyToManyField(Market, related_name='waiters_owned_by')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def get_full_name(self):
        """Return the full name for the user."""
        return self.full_name
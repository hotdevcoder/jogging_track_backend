from django.db import models
from django.db.models import Sum, Avg, Min, Max
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.utils.functional import cached_property
from datetime import date, timedelta
from math import ceil

# Create your models here.
class Entry(models.Model):
  distance = models.PositiveIntegerField(default = 0)
  duration = models.PositiveIntegerField(default = 1)
  date = models.DateField(auto_now_add = True)


ROLE_CHOICE = (
	(u'admin', 'Admin'),
	(u'manager', 'Manager'),
	(u'admin', 'Admin'),	
)

class UserQuerySet(models.QuerySet):
	def fillter_by_user(self, user):
		if user.is_admin:
			return self.filter(role__in=  ['admin', 'manager','user'])
		if user.is_manager:
			return self.filter(rolie__in = ['manager', 'user'])
		else:
			return self.filter(pk=user.pk)

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(_('First Name'), max_length=50)
	last_name = models.CharField(_('Last Name'), max_length=50)
	email = models.CharField(_('Email Adress'), max_length=50, unique=True)
	role = models.CharField(max_length=15, choices=ROLE_CHOICE, default='user')
	is_superuser = models.BooleanField(_('superuser status'), default=False)
	is_staff = models.BooleanField(_('staff status'), default=False)
	is_active = models.BooleanField(_('active'), default=True)
	USERNAME_FIELD = 'email'
	objects = UserManager()
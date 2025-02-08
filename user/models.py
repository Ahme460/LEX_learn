import pycountry
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have a username.')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email,username, password=None, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    @staticmethod
    def get_country():
        countries = list(pycountry.countries)
        country_choices = [(country.alpha_2, country.name) for country in countries]
        return country_choices

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    country = models.CharField(max_length=2, choices=get_country(), default='EG')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'



class UserDevice(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    device_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user_agent = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Contact(models.Model):
    email_1=models.CharField(max_length=500)
    email_2=models.CharField(max_length=500)
    telegram_link=models.URLField(max_length=500)
    facebook_kink=models.URLField(max_length=500)
    phone_number=models.CharField(max_length=100)
    


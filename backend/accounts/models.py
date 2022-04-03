from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser):
    phone_number = PhoneNumberField(
        unique=True, null=False, blank=False
    )
    first_name = models.CharField(
        max_length=256, default="", blank=True
    )
    last_name = models.CharField(
        max_length=256, default="", blank=True
    )
    national_code = models.CharField(
        max_length=16, unique=True, blank=False, null=False
    )
    joined_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    company = ... # foreginkey to haul.company
    otp = models.CharField(
        max_length=16, null=True, blank=True
    )
    password = None
    USERNAME_FIELD = 'phone_number'


    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_edited(self):
        return not self.edited_date == self.joined_date

    def __str__(self) -> str:
        return self.full_name

    __repr__ = __str__

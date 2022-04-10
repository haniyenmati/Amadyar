from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager as DjangoUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
import pyotp


class UserManager(DjangoUserManager):
    def create_user(self, phone_number):
        secret = pyotp.random_base32()
        otp =  pyotp.totp.TOTP(secret).now()
        user = User(phone_number=phone_number, otp=otp)
        user.set_unusable_password()
        user.save()
        print('otp is:', otp) # send sms
        return user


    def create_superuser(self,phone_number, password, **kwargs):
        user = User(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(
        unique=True, null=False, blank=False
    )
    first_name = models.CharField(
        max_length=256, default=str, blank=True
    )
    last_name = models.CharField(
        max_length=256, default=str, blank=True
    )
    joined_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    otp = models.CharField(
        max_length=6, null=True, blank=True,  default=str
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_edited(self):
        return not self.edited_date == self.joined_date

    def __str__(self) -> str:
        return self.full_name

    __repr__ = __str__

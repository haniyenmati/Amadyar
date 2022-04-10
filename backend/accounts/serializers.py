from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions
from django.contrib.auth.models import update_last_login
from accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField


class PhoneNumberSerializer(serializers.serializers.Serializer):
    phone_number = PhoneNumberField()

class SignupSerializer(serializers.serializers.ModelSerializer):
    company_code = serializers.serializers.CharField(required=True)
    class Meta:
        model = User
        fields =  ['phone_number', 'first_name', 'last_name', 'company_code']

class MyTokenObtainPairSerializer(serializers.TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp'] = serializers.PasswordField()
        del self.fields['password']

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'otp': attrs['otp']
        }

        if not PhoneNumberSerializer(data={"phone_number": authenticate_kwargs["phone_number"]}).is_valid():
            raise exceptions.NotAcceptable("invliad phone number")

        try:
            self.user = User.objects.get(phone_number=authenticate_kwargs["phone_number"])
        except:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        if self.user.otp != authenticate_kwargs["otp"]:
            raise exceptions.NotAcceptable("OTP does not match")

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        data = {}

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["phone_number"] = str(self.user.phone_number)
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["company"] = self.user.driver.company.name
        data["company_code"] = self.user.driver.company.company_code

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token['phonenumber'] = str(user.phone_number)

        return token

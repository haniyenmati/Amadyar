from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.models import update_last_login
from accounts.models import User, TempOTP
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

class SignupSerializer(serializers.ModelSerializer):
    company_code = serializers.CharField(required=True)
    class Meta:
        model = User
        fields =  ['phone_number', 'first_name', 'last_name', 'company_code']

class OTPCheckSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = TempOTP
        fields = ['phone_number', 'otp']

class MyTokenObtainPairSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    otp = serializers.CharField()

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

        data = {}

        token = self.get_token(self.user)

        data["token"] = str(token)
        data["phone_number"] = str(self.user.phone_number)
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["company"] = self.user.driver.company.name
        data["company_code"] = self.user.driver.company.company_code

        update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user: User):
        token, created = Token.objects.get_or_create(user=user)

        return token.key

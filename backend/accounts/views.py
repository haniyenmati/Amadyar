from django.db.transaction import atomic
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import MyTokenObtainPairSerializer, PhoneNumberSerializer, SignupSerializer
from accounts.models import User
from haul.models import Driver, Company
from accounts.services import SMSService, OTPService


class PhoneNumberCheck(GenericAPIView):
    def get_serializer_class(self):
        return PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'msg': 'already logged in'})

        serializer = PhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': 'invalid phone number'})
        
        phone_number = request.data.get('phone_number')
        user_exists = User.objects.filter(phone_number=phone_number).exists()
        otp = OTPService.generate_otp()

        if user_exists:
            user = User.objects.get(phone_number=phone_number)
            user.otp = otp
            user.save()
            SMSService().send_otp(phone=str(phone_number)[1:], otp=str(otp))
        
        return Response({'user_exists': user_exists})


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SignupView(GenericAPIView):
    def get_serializer_class(self):
        return SignupSerializer

    @atomic
    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return {'msg': 'already logged in'}

            company_code = request.data.pop('company_code')
            if not Company.objects.filter(company_code=company_code).exists():
                return Response({'msg': 'invalid company_code'})

            user = User(**request.data)
            user.save()

            company = Company.objects.get(company_code=company_code)
            driver = Driver(user=user, company=company)
            driver.save()

            user.otp = OTPService.generate_otp()
            user.save()
            SMSService().send_otp(phone=str(user.phone_number)[1:], otp=user.otp)

            return Response({
                'phone_number': str(user.phone_number),
                'full_name': user.full_name,
                'company': driver.company.name,
                'company_code': driver.company.company_code,
                'otp': user.otp
            })
        except Exception as err:
            return Response({'msg': str(err)})

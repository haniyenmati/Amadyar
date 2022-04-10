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
            return Response({'detail': 'already logged in'})

        serializer = PhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'detail': 'invalid phone number'})
        
        phone_number = request.data.get('phone_number')
        user_exists = User.objects.filter(phone_number=phone_number).exists()
        otp = OTPService.generate_otp()

        if user_exists:
            user = User.objects.get(phone_number=phone_number)
        else:
            user = User.objects.create_user(phone_number=phone_number)
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
                return {'detail': 'already logged in'}

            if not SignupSerializer(data=request.data).is_valid():
                return Response({'detail': 'invalid data'})

            company_code = request.data.pop('company_code')
            if not Company.objects.filter(company_code=company_code).exists():
                return Response({'detail': 'invalid company_code'})

            user = User(**request.data)
            user.save()

            company = Company.objects.get(company_code=company_code)
            driver = Driver(user=user, company=company)
            driver.save()

            return Response({
                'phone_number': str(user.phone_number),
                'full_name': user.full_name,
                'company': driver.company.name,
                'company_code': driver.company.company_code
            })
        except Exception as err:
            return Response({'detail': str(err)})

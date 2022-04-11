from django.db.transaction import atomic
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import MyTokenObtainPairSerializer, OTPCheckSerializer, PhoneNumberSerializer, SignupSerializer
from accounts.models import TempOTP, User
from haul.models import Driver, Company
from accounts.services import SMSService, OTPService


class PhoneNumberCheck(GenericAPIView):
    def get_serializer_class(self):
        return PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'already logged in'}, status=400)

        serializer = PhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'detail': 'invalid phone number'}, status=400)
        
        phone_number = request.data.get('phone_number')
        user_exists = User.objects.filter(phone_number=phone_number).exists()
        otp = OTPService.generate_otp()

        if user_exists:
            user = User.objects.get(phone_number=phone_number)
            user.otp = otp
            user.save()
        else:
            if TempOTP.objects.filter(phone_number=phone_number).exists():
                temp_otp = TempOTP.objects.get(phone_number=phone_number)
                temp_otp.otp = otp
            else:
                temp_otp = TempOTP(phone_number=phone_number, otp=otp)
            temp_otp.save()

        SMSService().send_otp(phone=str(phone_number)[1:], otp=str(otp))
        
        return Response({'user_exists': user_exists})


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class OTPCheckView(GenericAPIView):
    def get_serializer_class(self):
        return OTPCheckSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'already logged in'}, status=400)

        serializer = OTPCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'detail': 'invalid information(phone_number/otp)'}, status=400)

        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']
        phone_number_is_valid = TempOTP.objects.filter(phone_number=phone_number).exists()
        if not phone_number_is_valid:
            return Response({'detail': 'invalid phone number'}, status=400)

        temp_otp = TempOTP.objects.get(phone_number=phone_number)
        if temp_otp.otp == otp:
            return Response({'otp_is_valid': True}, status=200)
        return Response({'otp_is_valid': False}, status=400)
        

class SignupView(GenericAPIView):
    def get_serializer_class(self):
        return SignupSerializer

    @atomic
    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return Response({'detail': 'already logged in'}, status=400)

            if not SignupSerializer(data=request.data).is_valid():
                return Response({'detail': 'invalid data'}, status=400)

            company_code = request.data.get('company_code')
            if not Company.objects.filter(company_code=company_code).exists():
                return Response({'detail': 'invalid company_code'}, status=400)

            user = User(
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                phone_number=request.data['phone_number'])
            user.save()

            company = Company.objects.get(company_code=company_code)
            driver = Driver(user=user, company=company)
            driver.save()

            token = MyTokenObtainPairSerializer.get_token(user=user)

            return Response({
                'phone_number': str(user.phone_number),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'company': driver.company.name,
                'company_code': driver.company.company_code,
                'token': token
            })
        except Exception as err:
            return Response({'detail': str(err)}, status=400)

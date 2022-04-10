from django.urls import path
from accounts.views import PhoneNumberCheck, LoginView, SignupView

app_name = 'accounts'

urlpatterns = [
    path('phone_number/', PhoneNumberCheck.as_view(), name='phonenumber-check'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup')
]

import requests
import json
from pyotp import random_base32, TOTP


class SMSService:
    __api_key = "11TgeUybotjKAIzarfOEJXrXYbJcKHrhGsOD/qZ9FxU"
    sender_number = "30005006006885"

    def __request_builder(self, url, body):
        headers = {'apikey': self.__api_key}
        response = requests.post(url, headers=headers, data=body)

        if response.status_code != 200:
            raise Exception('bad status in sending otp message', response.status_code, response.text)

        if json.loads(response.text)['messageids'] < 1000:
            raise Exception('problem in sending otp sms', response.status_code, response.text)

        return response

    def send_otp(self, phone, otp):
        url = "http://api.ghasedaksms.com/v2/send/verify"
        body = {
            "param1": otp,
            "receptor": phone,
            "type": 1,
            "template": "amadyar"
        }
        self.__request_builder(url, body)


class OTPService:
    @classmethod
    def generate_otp(cls):
        return str(TOTP(random_base32()).generate_otp(6))


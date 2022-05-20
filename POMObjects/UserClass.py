import random
import string

from POMObjects import endpoints
from POMObjects.BaseClass import BaseApi
from Utils.Methods import APIRequest
from config import BASE_URL
import config
import requests
global access_token


class Users(BaseApi):

    def __init__(self):
        super().__init__()
        self.base_url = BASE_URL
        self.request = APIRequest()

    def create_user(self, body=None):
        email = "Test_Uer_{0}@hashedIn.com".format(random.randint(10000, 100000))
        config.EMAIL = email
        payload = {
            "name": "Test_User_{0}".format("".join(random.choices(string.ascii_uppercase + string.digits, k=6))),
            "email": email,
            "password": "12345678",
            "age": random.randint(20, 60)
        }
        response = self.request.post(endpoints.register_user.format(self.base_url), payload, self.headers)
        config.ACCESS_TOKEN = response.as_dict['token']
        return response

    def get_user(self):
        response = self.request.get(endpoints.get_user.format(self.base_url), self.request.headers(config.ACCESS_TOKEN))
        return response

    def login(self):
        payload = {
            "email": config.EMAIL,
            "password": "12345678"
        }
        response = self.request.post(endpoints.login.format(self.base_url), payload, self.headers)
        return response

    def duplicate_user(self, duplicate_payload):
        payload = {
            "name": duplicate_payload["name"],
            "email": duplicate_payload["email"],
            "password": "12345678",
            "age": duplicate_payload["age"]
        }
        response = self.request.post(endpoints.register_user.format(self.base_url), payload, self.headers)
        return response

    def validate_token(self, token='abcd'):
        response = self.request.get(endpoints.get_user.format(self.base_url), self.request.headers(token))
        return response


import random
import string
import config
from POMObjects import endpoints
from POMObjects.BaseClass import BaseApi
from Utils.Methods import APIRequest
from config import BASE_URL
import requests
from Utils.Read_Write_xlsx import XlsxReader

rd = XlsxReader()


class Tasks(BaseApi):

    def __init__(self):
        super().__init__()
        self.base_url = BASE_URL
        self.request = APIRequest()

    def add_task(self):
        payload = {
            "description": random.choice(config.TASKS_TO_DO)
        }
        response = self.request.post(endpoints.task.format(self.base_url), payload, self.request.headers(config.ACCESS_TOKEN))
        return response

    def add_multiple_tasks(self, no_of_tasks=21):
        for i in range(0, no_of_tasks):
            response = self.add_task()
            rd.write_data(config.EMAIL, response)
        rd.merge_cells()

    def pagination(self, limit, skip=10):
        response = self.request.get(endpoints.get_task_by_pagination.format(self.base_url, limit, skip), self.request.headers(config.ACCESS_TOKEN))
        return response

    def get_all_tasks(self):
        response = self.request.get(endpoints.get_all_tasks.format(self.base_url), self.request.headers(config.ACCESS_TOKEN))
        return response

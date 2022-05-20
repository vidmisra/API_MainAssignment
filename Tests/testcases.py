import pytest

import Tests.asserts
import config
from POMObjects.Tasks import Tasks
from POMObjects.UserClass import Users
from Tests.BaseTest import BaseTest
from Tests.asserts import Asserts

users = Users()
tasks = Tasks()
pytestmark = [pytest.mark.P1, pytest.mark.negative]

@pytest.mark.usefixtures("setup")
class TestFeatures(BaseTest):

    @pytest.mark.P1
    def test_user_is_created(self, config):
        log = self.getLogger()
        response = users.create_user()
        try:
            Asserts.assert_code_status(response, 201)
            Asserts.assert_response_content_type(response)
            log.info("Status code is {0}.\nUser created successfully".format(response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

        get_response = users.get_user()
        try:
            assert (response.as_dict["user"]["name"] == get_response.as_dict["name"])
            assert (response.as_dict["user"]["email"] == get_response.as_dict["email"])
            assert (response.as_dict["user"]["age"] == get_response.as_dict["age"])
            log.info(
                "\nUser Data:\nName: {0}\nEmail: {1}\n".format(response.as_dict["user"]["name"],
                                                              response.as_dict["user"]["email"]))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    @pytest.mark.P2
    @pytest.mark.negative
    def test_duplicate_user_creation(self):
        """Duplicate check for same User"""
        log = self.getLogger()
        get_response = users.get_user()
        duplicate_response = users.duplicate_user(get_response.as_dict)
        try:
            Asserts.assert_code_status(duplicate_response, 400)
            log.info("\nDuplicate user not allowed\nStatus code :" + str(duplicate_response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    @pytest.mark.P1
    def test_user_login(self):
        log = self.getLogger()
        response = users.login()
        try:
            Asserts.assert_code_status(response, 200)
            Asserts.assert_response_content_type(response)
            log.info("\nLogin successful\nStatus code :" + str(response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    @pytest.mark.P1
    def test_add_task(self):
        log = self.getLogger()
        response = tasks.add_task()
        try:
            Asserts.assert_code_status(response, 201)
            Asserts.assert_response_content_type(response)
            log.info("\nFollowing Tasks are added successfully\nTask Added--" + str(response.as_dict["data"]["description"]))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    @pytest.mark.P1
    def test_add_multiple_tasks(self):
        list_of_tasks=[]
        log = self.getLogger()
        tasks.add_multiple_tasks()
        response = tasks.get_all_tasks()
        try:
            Asserts.assert_code_status(response, 200)
            assert (response.as_dict['count'] == 22)
            log.info("Count of Tasks:" + str(response.as_dict['count']))
            for task in response.as_dict['data']:
                assert task["completed"] is False
                assert task["description"] in config.TASKS_TO_DO
                list_of_tasks.append(str(task["description"]))
            log.info("\nFollowing Tasks are added successfully\nTask Added--".join(list_of_tasks))
        except AssertionError as err:
            log.exception(str(err))
            raise err

    @pytest.mark.P1
    def test_validate_pagination(self):
        log = self.getLogger()
        limits = [2, 5, 6]
        try:
            for limit in limits:
                list_of_tasks=[]
                response = tasks.pagination(limit)
                Asserts.assert_code_status(response, 200)
                Asserts.assert_response_content_type(response)
                log.info("Pagination limit :" + str(limit))
                for task in response.as_dict['data']:
                    assert task["completed"] is False
                    assert task["description"] in config.TASKS_TO_DO
                    list_of_tasks.append(str(task["description"]))
            log.info("\nFollowing Tasks are added successfully\nTask Added--".join(list_of_tasks))
        except Exception as e:
            log.info(str(e))
            raise e

    @pytest.mark.P2
    @pytest.mark.negative
    def test_validate_incorrect_token(self):
        """Validating the Authentication for incorrect token"""
        log = self.getLogger()
        response = users.validate_token()
        try:
            Asserts.assert_code_status(response, 401)
            Asserts.assert_response_content_type(response)
            log.info("User not authenticated: Status Code:" + str(response.status_code))
        except AssertionError as err:
            log.exception(str(err))
            raise err

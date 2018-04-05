import sys


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver



class FunctionalTestsBase(StaticLiveServerTestCase):



    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()




    # @classmethod
    # def setUpClass(cls):
    #     for arg in sys.argv:
    #         if 'liveserver' in arg:
    #             cls.server_url = 'http://' + arg.split('=')[1]
    #             return
    #         super().setUpClass()
    #         cls.server_url = cls.live_server_url
    #
    # @classmethod
    # def tearDownClass(cls):
    #     if cls.server_url == cls.live_server_url:
    #         super().tearDownClass()
    #
    # def setUp(self):
    #     # from employees.models import Employee
    #     # zbigniew_adamski = Employee.objects.get(id=3)
    #     # assert ('Zbigniew Adamski' == str(
    #     #     zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'
    #     self.browser = webdriver.Firefox()
    #     self.browser.implicitly_wait(3)
    #
    # def tearDown(self):
    #     self.browser.quit()

import os
from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from polishlody.settings import BASE_DIR


@override_settings(DEBUG=True, STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles'), )
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

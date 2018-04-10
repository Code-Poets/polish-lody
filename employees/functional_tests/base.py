import os
from selenium.webdriver.common.keys import Keys
import time
from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from polishlody.settings import BASE_DIR

# STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles'),

@override_settings(DEBUG=True)
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

    def log_manager_and_go_to_employee_list(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        login_field = self.selenium.find_element_by_id('id_username')
        password_field = self.selenium.find_element_by_id('id_password')
        login_field.send_keys('pawel.kisielewicz@codepoets.it')
        password_field.send_keys('codepoets')
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)
        employee_list_link = self.selenium.find_element_by_id('employees_link')
        employee_list_link.click()
        time.sleep(1)

    def log_employee_and_go_to_employee_list(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        login_field = self.selenium.find_element_by_id('id_username')
        password_field = self.selenium.find_element_by_id('id_password')
        login_field.send_keys('pawel@wp.pl')
        password_field.send_keys('codepoets')
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)
        employee_list_link = self.selenium.find_element_by_id('my-details-link')
        employee_list_link.click()
        time.sleep(1)

    def logout(self):
        button = self.selenium.find_element_by_id('logout-button')
        button.click()


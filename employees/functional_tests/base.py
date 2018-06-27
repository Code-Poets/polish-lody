import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver


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
        login_field.send_keys('manager@polishlody.pl')
        password_field.send_keys('codepassword')
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)
        employee_list_link = self.selenium.find_element_by_id('employees_link')
        employee_list_link.click()
        time.sleep(1)
        self.__change_lang_to_pl()

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
        self.__change_lang_to_pl()

    def logout(self):
        button = self.selenium.find_element_by_id('logout-button')
        button.click()

    def __change_lang_to_pl(self):
        if 'Employee list' in self.selenium.title:
            button = self.selenium.find_element_by_id('change-language')
            button.click()

        if 'Details' in self.selenium.title:
            button = self.selenium.find_element_by_id('change-language')
            button.click()

import sys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from unittest2 import skip, TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.support import expected_conditions as EC

from employees.functional_tests.base import FunctionalTestsBase



class UserLogin(LiveServerTestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_user_schould_login(self):
        self.browser.get('%s%s' % (self.live_server_url, ''))
        self.assertIn('Witajcie', self.browser.title)
        login_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')

        login_field.send_keys('pawel.kisielewicz@codepoets.it')
        password_field.send_keys('codepoets')
        password_field.send_keys(Keys.ENTER)
        time.sleep(2)
        self.assertIn('Panel główny', self.browser.title)
        employee_list_link = self.browser.find_element_by_id('employees_link')
        employee_list_link.click()
        self.assertIn('Lista Pracowników', self.browser.title)


class ListViewFilter(FunctionalTestsBase):
    selenium = None
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']


    def __log_manager_and_go_to_employee_list(self):
        self.selenium.get('%s%s' % (self.live_server_url, ''))
        login_field = self.selenium.find_element_by_id('id_username')
        password_field = self.selenium.find_element_by_id('id_password')
        login_field.send_keys('pawel.kisielewicz@codepoets.it')
        password_field.send_keys('codepoets')
        password_field.send_keys(Keys.ENTER)
        time.sleep(2)
        employee_list_link = self.selenium.find_element_by_id('employees_link')
        employee_list_link.click()
        time.sleep(4)


    def test_sale_filter(self):
        self.__log_manager_and_go_to_employee_list()
        self.assertIn('Lista Pracowników', self.selenium.title)

        current_emp_cb = self.selenium.find_element_by_id('current_employees_id')
        sale_emp_cb = self.selenium.find_element_by_id('pos_sale')

        time.sleep(2)

        # paginate_previous_radio = self.selenium.find_element_by_id('pg-previous')
        paginate_previous_radio = self.selenium.find_element_by_class_name('paginated')
        # paginate_previous_radio = self.selenium.find_element_by_class_name('my-button previous disabled')

        sale_emp_label_clickable = self.selenium.find_element_by_id('pos_sale_label')


        sale_emp_label_clickable.click()

        self.assertTrue(current_emp_cb.is_selected())
        self.assertTrue(sale_emp_cb.is_selected())
        self.assertFalse(paginate_previous_radio.is_selected())



    def test_employee_message(self):
        self.__log_manager_and_go_to_employee_list()

        # poprawić, żby przejście było przez kliknięcia a nie przekierowanie
        self.assertIn('Lista Pracowników', self.selenium.title)
        self.selenium.get('%s%s' % (self.live_server_url, '/employees/30'))
        self.assertIn('Detale', self.selenium.title)

        row = self.selenium.find_element_by_class_name('details')
        rows = self.selenium.find_elements_by_class_name('details')


        # time.sleep(400)

        message_march_2018 = self.selenium.find_element_by_id('month_message33')
        message_march_2018.click()
        time.sleep(2)
        alert = self.selenium.switch_to_alert()


        month_message=alert.driver.page_source

        self.assertIn('pracowalem wiecej',month_message)











#
# @skip
# class NewVisitorTest(FunctionalTests):
#
#     def test_can_start_a_list_and_retrieve_it_later(self):
#         self.browser.get(self.server_url)
#         self.assertIn('Listy', self.browser.title)
#         header_text = self.browser.find_element_by_tag_name('h1').text
#         self.assertIn('listę', header_text)
#
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         self.assertEqual(inputbox.get_attribute('placeholder'), 'Wpisz rzeczy do zrobienia')
#
#         inputbox.send_keys('Kupić pawie pióra')
#         inputbox.send_keys(Keys.ENTER)
#         time.sleep(3)
#
#         edith_list_url = self.browser.current_url
#         self.assertRegex(edith_list_url, 'lists/.+')
#
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
#         inputbox.send_keys(Keys.ENTER)
#         time.sleep(3)
#
#         self.check_for_row_in_list_table('1: Kupić pawie pióra')
#         self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')
#
#         self.browser.quit()
#         time.sleep(1)
#         self.browser = webdriver.Firefox()
#
#         # Franek wchodzi na stronę główną, nie ma śladów Edyty
#         self.browser.get(self.server_url)
#         page_text = self.browser.find_element_by_tag_name('body').text
#         self.assertNotIn('Kupić pawie pióra', page_text)
#         self.assertNotIn('zrobienia przynęty', page_text)
#
#         # Franek tworzy swoją listę, dodaje nowy element
#         inputbox = self.browser.find_element_by_id('id_new_item')
#         inputbox.send_keys('Kupić mleko')
#         inputbox.send_keys(Keys.ENTER)
#
#         # Franek dostaje swój URL
#         francis_list_url = self.browser.current_url
#         time.sleep(2)
#
#         # self.assertRegex(francis_list_url, 'lists/.+')
#         self.assertNotEqual(francis_list_url, edith_list_url)
#
#         page_text = self.browser.find_element_by_tag_name('body').text
#         self.assertNotIn('Kupić pawie pióra', page_text)
#         self.assertIn('Kupić mleko', page_text)

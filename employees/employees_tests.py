import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest2 import skip, TestCase

class UserLogin(StaticLiveServerTestCase):

    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']



    #
    # def setUp(self):
    #     self.browser = webdriver.Firefox()
    #     self.browser.implicitly_wait(2)
    #
    #
    # def tearDown(self):
    #     self.browser.quit()


    def test_user_schould_login(self):
        pass
    #
    #     current_url= self.browser.current_url
    #     self.assertIn('Listy', self.browser.title)
    #     header_text = self.browser.find_element_by_tag_name('h1').text
    #     self.assertIn('listę', header_text)
    # #     # self.browser.get(self.server_url)
    #
    #
    #






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

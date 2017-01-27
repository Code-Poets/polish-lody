from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import TestCase, Client, RequestFactory

class SeleniumScriptTests(TestCase):
    driver = webdriver.Firefox()

    def test_should_submit_delay_script_work(self):

        self.driver.get("http://127.0.0.1:8000/")
        login_element = self.driver.find_element_by_id("id_username")
        pass_element = self.driver.find_element_by_id("id_password")
        login_element.send_keys("admin@polishlody.pl")
        pass_element.send_keys("codepassword")
        submit_element = self.driver.find_element_by_class_name("btn-primary")
        submit_element.click()
        time.sleep(3)
        self.driver.get("http://127.0.0.1:8000/employees/")
        # with open('jquery.min.js', 'r') as jquery_js: #read the jquery from a file
        #     jquery = jquery_js.read()
        #     self.driver.execute_script(jquery)
        time.sleep(1.5)
        sale = self.driver.find_element_by_name("position_sale")
        sale.click()
        time.sleep(2.5)
        sale = self.driver.find_element_by_name("position_sale")
        time.sleep(4)
        sale.click()
        other = self.driver.find_element_by_name("position_other")
        production = self.driver.find_element_by_name("position_production")
        other.click()
        time.sleep(0.5)
        production.click()
        time.sleep(3)
        unpaid = self.driver.find_element_by_id("chk_unpaid")
        unpaid.click()
        time.sleep(3)
        unpaid = self.driver.find_element_by_id("chk_unpaid")
        unpaid.click()
        other = self.driver.find_element_by_name("position_other")
        production = self.driver.find_element_by_name("position_production")
        other.click()
        time.sleep(0.5)
        production.click()
        paid = self.driver.find_element_by_id("chk_paid")
        paid.click()
        time.sleep(3)
        paid = self.driver.find_element_by_id("chk_paid")
        paid.click()
        text_input = self.driver.find_element_by_name("employee_filter")
        text_input.send_keys("ż")
        time.sleep(0.600)
        text_input.send_keys("u")
        time.sleep(0.600)
        text_input.send_keys("l")


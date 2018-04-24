import time
from enum import Enum
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
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

        login_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')

        login_field.send_keys('manager@polishlody.pl')
        password_field.send_keys('codepassword')
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)

        if 'Manager dashboard' in self.browser.title:
            button = self.browser.find_element_by_id('change-language')
            button.click()

        self.assertIn('Panel główny', self.browser.title, 'prawdopodobny problem z logowaniem')
        employee_list_link = self.browser.find_element_by_id('employees_link')
        employee_list_link.click()
        self.assertIn('Lista Pracowników', self.browser.title)


class ListViewFilter(FunctionalTestsBase):
    selenium = None
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    def test_sale_filter(self):
        self.log_manager_and_go_to_employee_list()
        self.assertIn('Lista Pracowników', self.selenium.title)
        sale_emp_label_clickable = self.selenium.find_element_by_id('pos_sale_label')

        self.__check_if_previous_page_exist_and_is_disabled()
        self.__check_if_next_page_exist_and_is_clickable()
        self.assertTrue(self.__check_page_exist_and_get_true_if_selected(1))
        self.assertFalse(self.__check_page_exist_and_get_true_if_selected(2))
        self.__check_if_per_page_exist_and_check_if_given_value_is_selected(10)

        names = ['Adamski Zbigniew', 'Lodziarz Czarny', 'Rrr Rrr']
        self.assertTrue(self.__check_employee_list_and_return_boolean_status(names))

        names = ['Sss Sss', 'Testowy Paweł', 'Testowyy Paweltest']
        self.assertFalse(self.__check_employee_list_and_return_boolean_status(names))
        self.assertEqual(self.__get_number_of_employees_on_current_page(), 10)

        sale_emp_label_clickable.click()

        self.assertTrue(self.__check_if_employee_filter_exist_and_get_boolean_value(EmployeeFilters.CURRENT_EMPLOYEES))
        self.assertTrue(self.__check_if_employee_filter_exist_and_get_boolean_value(EmployeeFilters.POS_SALE))
        self.__check_if_pagination_block_doesnt_exist()
        self.__check_if_per_page_exist_and_check_if_given_value_is_selected(10)

        names = ['Adamski Zbigniew']
        self.assertTrue(self.__check_employee_list_and_return_boolean_status(names))
        self.assertEqual(self.__get_number_of_employees_on_current_page(), 1)

        sale_emp_label_clickable.click()
        time.sleep(1)
        page_2_label_clickable = self.selenium.find_element_by_id('pg-label2-not-checked')
        page_2_label_clickable.click()

        self.__check_if_previous_page_exist_and_is_clickable()
        self.__check_if_next_page_exist_and_is_disabled()
        self.assertTrue(self.__check_page_exist_and_get_true_if_selected(2))
        self.assertFalse(self.__check_page_exist_and_get_true_if_selected(1))
        self.__check_if_per_page_exist_and_check_if_given_value_is_selected(10)
        names = ['Sss Sss', 'Testowy Paweł', 'Testowyy Paweltest']
        self.assertTrue(self.__check_employee_list_and_return_boolean_status(names))
        self.assertEqual(self.__get_number_of_employees_on_current_page(), 3)

    def __check_employee_list_and_return_boolean_status(self, list_given_by_tester):
        elements = self.selenium.find_elements_by_name('employee-from-list')
        employees_list = []

        for element in elements:
            employees_list.append(element.text)

        for name in list_given_by_tester:
            if name not in employees_list:
                return False
        return True

    def __get_number_of_employees_on_current_page(self):
        elements = self.selenium.find_elements_by_name('employee-from-list')
        return len(elements)

    def __check_if_employee_filter_exist_and_get_boolean_value(self, filter_name_enum):

        filter_name = filter_name_enum.value

        number_of_elements = len(self.selenium.find_elements_by_id(filter_name))
        self.assertNotEqual(number_of_elements, 0, 'unable to find ' + filter_name)

        element = self.selenium.find_element_by_id(filter_name)
        return element.is_selected()

    def __check_if_pagination_block_doesnt_exist(self):
        number_of_elements = len(self.selenium.find_elements_by_id('paginated'))
        self.assertEqual(number_of_elements, 0, 'pagination plock exist but it should not')

    def __check_if_previous_page_exist_and_is_disabled(self):
        number_of_elements = len(self.selenium.find_elements_by_xpath('//label[@class="my-button previous disabled"]'))
        self.assertNotEqual(number_of_elements, 0, 'unable to find previous page label with status disabled')

    def __check_if_previous_page_exist_and_is_clickable(self):
        number_of_elements = len(self.selenium.find_elements_by_xpath('//label[@class="my-button previous clickable"]'))
        self.assertNotEqual(number_of_elements, 0, 'unable to find previous page label with status clickable')

    def __check_if_next_page_exist_and_is_disabled(self):
        number_of_elements = len(self.selenium.find_elements_by_xpath('//label[@class="my-button next disabled"]'))
        self.assertNotEqual(number_of_elements, 0, 'unable to find next page label with status disabled')

    def __check_if_next_page_exist_and_is_clickable(self):
        number_of_elements = len(self.selenium.find_elements_by_xpath('//label[@class="my-button next clickable"]'))
        self.assertNotEqual(number_of_elements, 0, 'unable to find next page label with status clickable')

    def __check_page_exist_and_get_true_if_selected(self, number):

        element_id = 'pg-label' + str(number) + '-checked'
        number_of_elements = len(self.selenium.find_elements_by_id(element_id))
        if number_of_elements == 1:
            return True

        element_id = 'pg-label' + str(number) + '-not-checked'
        number_of_elements = len(self.selenium.find_elements_by_id(element_id))
        if number_of_elements == 1:
            return False
        else:
            raise NoSuchElementException('unable to find page radio number ' + str(number))

    def __check_if_per_page_exist_and_check_if_given_value_is_selected(self, per_page):
        element = self.selenium.find_elements_by_xpath('//li[@class="page-no active"]')
        element1 = self.selenium.find_elements_by_id('per-page-' + str(per_page))
        self.assertNotEqual(element, None, 'unable to find per page block')
        self.assertEqual(element, element1, 'given per_page is not selected')


class EmployeeMessage(FunctionalTestsBase):
    selenium = None
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    def test_employee_message(self):
        self.log_employee_and_go_to_employee_list()
        approve42 = self.selenium.find_element_by_id('month-approve-id42')
        approve42.click()

        submit_button = self.selenium.find_element_by_xpath('//input[@class="btn btn-primary"]')
        submit_button.click()

        approve43 = self.selenium.find_element_by_id('month-not-approve-id43')
        approve43.click()

        message_area = self.selenium.find_element_by_id('employee_message_id')
        message_area.send_keys('pracowałem więcej godzin w piątek 13-tego')
        submit_button = self.selenium.find_element_by_xpath('//input[@class="btn btn-primary"]')
        submit_button.click()

        message_month43 = self.selenium.find_element_by_id('month_message43')
        message_month43.click()
        alert = self.selenium.switch_to_alert()
        month_message = alert.driver.page_source

        self.assertIn('pracowałem więcej godzin w piątek 13-tego', month_message)

        self.logout()

        self.log_manager_and_go_to_employee_list()
        self.assertIn('Lista Pracowników', self.selenium.title)

        self.selenium.get('%s%s' % (self.live_server_url, '/employees/30'))
        self.assertIn('Detale', self.selenium.title)

        accepted_months = self.selenium.find_elements_by_xpath('//tr[@class="details"]')
        not_accepted_months = self.selenium.find_elements_by_xpath('//tr[@class="details unpaid"]')

        self.assertEqual(len(accepted_months), 2)
        self.assertEqual(len(not_accepted_months), 8)

        not_accepted_text = ''
        for month in not_accepted_months:
            not_accepted_text = not_accepted_text + str(month.text)

        self.assertIn('Listopad', not_accepted_text)
        self.assertIn('Marzec', not_accepted_text)
        self.assertIn('Lipiec', not_accepted_text)

        accepted_text = ''
        for month in accepted_months:
            accepted_text = accepted_text + str(month.text)

        self.assertIn('Październik', accepted_text)
        self.assertIn('Czerwiec', accepted_text)

        message_month43 = self.selenium.find_element_by_id('month_message43')
        message_month43.click()
        time.sleep(1)

        alert = self.selenium.switch_to_alert()
        month_message = alert.driver.page_source
        time.sleep(1)
        self.assertIn('pracowałem więcej godzin w piątek 13-tego', month_message)


class EmployeeFilters(Enum):
    POS_SALE = 'pos_sale'
    POS_PRODUCTION = 'pos_production'
    POS_OTHER = 'pos_other'
    PAID = 'chk_paid'
    NOT_PAID = 'chk_unpaid'
    FORMER_EMPLOYEES = 'former_employees_id'
    CURRENT_EMPLOYEES = 'current_employees_id'

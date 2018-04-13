from django.contrib.auth import get_user_model
from unittest2 import skip

from users.models import MyUser
from django.test import TestCase, Client, RequestFactory, TransactionTestCase
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from datetime import datetime, timedelta, date
from .models import City, Employee, Month
from datetime import datetime, date
import random
import time

# FIXME: This method should not be applied globally(@Kamil)
User = get_user_model()


# FIXME: Admin should be loaded from fixtures
def admin_login(self):
    admin = User.objects.create_superuser(email="test_admin@polishlody.pl", password="codepassword")
    admin.save()
    return self.client.login(username='test_admin@polishlody.pl', password='codepassword')


class EmployeeMethodTests(TestCase):
    start_date = date.today()
    exp_date = date.today() + timedelta(days=30)

    def test_full_name_with_valid_employee(self):
        """
        the full_name method should return joined (' ') first_name and last_name
        """
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        e = Employee(first_name='John', last_name='Gamlet', email="gamlet@example.com", contract_start_date=start_date,
                     contract_exp_date=exp_date)
        self.assertEqual(e.full_name(), "Gamlet John")

    def test_create_new_employee_with_empty_attributes(self):
        """
        saving employee without all required data should be aborted
        """
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        with self.assertRaises(IntegrityError):
            Employee(first_name=None, last_name=None, email=None, contract_start_date=start_date,
                     contract_exp_date=exp_date).save()


class EmployeeListViewTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_user_should_login_successful(self):
        is_logged = self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        self.assertEqual(is_logged, True)

    def test_employees_list_view_should_contain_employee_from_fixtury(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        response = self.client.get(reverse_lazy('employees'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zbigniew Adamski')

    def test_employee_list_view_should_be_paginated_ordered_and_filtered_by_default(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')

        response = self.client.get(reverse_lazy('employees'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(response.context['current_employees'], True)
        self.assertContains(response, 'Zbigniew Adamski')
        self.assertContains(response, 'Czarny Lodziarz')
        self.assertContains(response, 'Rrr Rrr')
        self.assertEqual(response.context['orderby'], 'last_name')
        self.assertEqual(response.context['page'], 1)
        self.assertEqual(response.context['per_page'], 10)

    def test_employee_list_view_should_changed_by_ajax_sale_current(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')

        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'position_sale': 'on',
                    'current_employees': 'on',
                    'per_page': '10',
                    }

        response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ajax_request'], True)
        self.assertContains(response, 'Zbigniew Adamski')
        paginator = response.context['paginator']
        self.assertEqual(paginator.per_page, 10)
        self.assertEqual(len(response.context['page_employee_list']), 1)
        self.assertEqual(response.context['orderby'], 'last_name')

    def test_employee_list_view_should_changed_by_ajax_paid_current_pagination(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')

        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'order': 'rate_per_hour',
                    'hide_zero_salary_months': 'on',
                    'current_employees': 'on',
                    'per_page': '5',
                    'page': '2',
                    }

        response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ajax_request'], True)
        self.assertContains(response, 'Mmm Mmm')
        self.assertContains(response, 'Waldemar Kiepski')
        paginator = response.context['paginator']
        self.assertEqual(paginator.per_page, 5)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(response.context['page_employee_list']), 5)
        self.assertEqual(response.context['orderby'], 'rate_per_hour')


class EmployeeDetailViewTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_employee_detail_view_with_the_existing_record(self):
        url = reverse_lazy('employee_detail', args=(30,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testowyy Paweltest")
        self.assertContains(response, "pawel@wp.pl")

    def test_employee_message_view_with_the_existing_record(self):
        url = reverse_lazy('employee_message', args=(47,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nie zgadzam sie")

    def test_should_employee_detail_view_show_correct_amount_of_months(self):
        url = reverse_lazy('employee_detail', args=(29,))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['months'],
            ['<Month: February 2018>',
             '<Month: January 2018>', ]
        )

    def test_should_employee_detail_view_be_paginated(self):
        url = reverse_lazy('employee_detail', args=(30,))
        response = self.client.get(url)

        paginator = response.context['paginator']
        self.assertEqual(paginator.per_page, 10)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(response.context['object_list']), 10)

        url = reverse_lazy('employee_detail', args=(30,)) + "?page=2&per_page=10"
        response = self.client.get(url)

        paginator = response.context['paginator']
        self.assertEqual(paginator.per_page, 10)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_should_month_create_view_work(self):
        url = reverse_lazy('employee_detail', args=(29,))

        from employees.forms import MonthForm
        form = MonthForm({
            'year': '2018',
            'month': '3',
            'salary_is_paid': False,
            'hours_worked_in_this_month': '150',
            'rate_per_hour_this_month': '15',
            'bonuses': '100',
        })

        self.assertTrue(form.is_valid())
        march2018 = form.save()

        self.assertEqual(march2018.year, 2018)
        self.assertEqual(march2018.month, 3)
        self.assertEqual(march2018.salary_is_paid, False)
        self.assertEqual(march2018.rate_per_hour_this_month, 15)


class EmployeeMessageViewTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_should_message_view_work_properly(self):
        url = reverse_lazy('employee_message', args=(44,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bo nie")


class MonthCreateAndUpdateAndDeleteViewTests(TransactionTestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_should_month_save_and_delete_method_work_properly(self):

        emp = Employee.objects.get(pk=30)
        self.assertEqual(emp.month_set.all().count(), 12)

        m = Month(year=2185, month=11, rate_per_hour_this_month=10,
                  hours_worked_in_this_month=300, employee=emp)
        m.save()
        m2 = Month(year=2186, month=7, rate_per_hour_this_month=10,
                   hours_worked_in_this_month=150, employee=emp, salary_is_paid=True)
        m2.save()
        self.assertEqual(emp.month_set.all().count(), 14)
        self.assertEqual(m.calculating_salary_for_this_month(), 3000)
        self.assertEqual(m.month_name(), 'November')
        self.assertEqual(m.month_detail(), '2185 November')
        fail_month = Month(year=2185, month=11, rate_per_hour_this_month=10,
                           hours_worked_in_this_month=300, employee=emp)
        self.assertEqual(emp.all_unpaid_salaries(), 14800)
        try:
            fail_month.save()
        except IntegrityError:
            print("Unique together constraint raises IntegrityError as expected.")

        months = Month.objects.filter(year__gte=2185)
        self.assertEqual(months.count(), 2)
        month1_id = months[0].id

        response = self.client.get(reverse('month_delete', args=(month1_id,)), follow=True)
        self.assertTrue('Are you sure you want to delete' in str(response.content))

        months.delete()

        months_after_delete = Month.objects.filter(year__gte=2185)
        self.assertEqual(months_after_delete.count(), 0)

        response404 = self.client.get(reverse('month_delete', args=(month1_id,)), follow=True)
        self.assertTrue('404' in str(response404.content))

    def test_should_month_update_view_work(self):

        month = random.choice(Month.objects.all())
        employee = month.employee  # .__str__()
        year = month.year
        url = reverse_lazy('month_edit', args=(month.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['month'], month)
        initial_form_data = response.context['form']
        self.assertTrue('selected="selected">%s<' % (employee) in str(initial_form_data['employee']))
        self.assertTrue('type="number" value="%d" required' % (year) in str(initial_form_data['year']))
        self.assertTrue('type="number" value="%s" required' %
                        (month.rate_per_hour_this_month) in
                        str(initial_form_data['rate_per_hour_this_month']))

    def test_should_employee_delete_method_work_properly(self):
        response = self.client.get(reverse('employee_delete', args=(30,)), follow=True)
        self.assertTrue('Are you sure you want to delete' in str(response.content))
        self.client.post(reverse('month_delete', args=(44,)), follow=True)

        TestowyyPaweltest = Employee.objects.get(pk=30)
        TestowyyPaweltest.delete()

        response404 = self.client.get(reverse('month_delete', args=(44,)), follow=True)
        self.assertTrue('does not exist' in str(response404.content))


class EmployeeFilterTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_should_name_filter_work_properly(self):
        admin_login(self)
        url = reverse_lazy('employees')
        response = self.client.get(url)
        filtered_response = self.client.get(url + "?employee_filter=czarny")
        self.assertQuerysetEqual(
            filtered_response.context['page_employee_list'],
            ['<Employee: Czarny Lodziarz>']
        )
        filtered_response_multiple_results = self.client.get(url + "?employee_filter=w")
        self.assertQuerysetEqual(
            filtered_response_multiple_results.context['page_employee_list'],
            ['<Employee: Zbigniew Adamski>', '<Employee: Waldemar Kiepski>', '<Employee: Paweł Testowy>',
             '<Employee: Paweltest Testowyy>']
        )
        filtered_response_none = self.client.get(url + "?employee_filter=inexistent_potato")
        self.assertQuerysetEqual(
            filtered_response_none.context['page_employee_list'],
            []
        )
        self.assertTrue("No employee meets the search criteria." in str(filtered_response_none.content))

    def test_should_position_other_filter_work_properly(self):
        """
        Be careful with tests no ajax requests. ListView sets current_employees True as default, all not ajax requests
        are checked- if there is no session value default value is set as True. Default pagination is 10.
        """

        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'position_other': 'on',
                    'current_employees': 'on',
                    'per_page': '10',
                    }

        position_response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(position_response.status_code, 200)
        self.assertEqual(position_response.context['ajax_request'], True)
        self.assertContains(position_response, 'Waldemar Kiepski')
        self.assertContains(position_response, 'Nnn Nnn')
        self.assertContains(position_response, 'Testowy Paweł')
        self.assertNotContains(position_response, 'Eee Eee')
        self.assertNotContains(position_response, 'Jjj Jjj')

    def test_should_position_paid_filter_work_properly(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'hide_zero_salary_months': 'on',
                    'per_page': '5',
                    }

        position_response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(position_response.status_code, 200)
        self.assertEqual(position_response.context['ajax_request'], True)
        self.assertContains(position_response, 'Aaa Aaa')
        self.assertContains(position_response, 'Ccc Ccc')
        self.assertContains(position_response, 'Eee Eee')
        self.assertNotContains(position_response, 'Fff Fff')

    def test_should_position_former_filter_work_properly(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'former_employees': 'on',
                    'per_page': '5',
                    'page': '2',
                    }

        position_response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(position_response.status_code, 200)
        self.assertEqual(position_response.context['ajax_request'], True)
        self.assertContains(position_response, 'Iii Iii')
        self.assertContains(position_response, 'Ggg Ggg')
        self.assertContains(position_response, 'Eee Eee')
        self.assertNotContains(position_response, 'Waldemar Kiepski')

    def test_should_order_filter_work_properly(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'order': 'contract_exp_date',
                    'hide_paid_employees_filter': 'on',
                    'current_employees': 'on',
                    'per_page': '5',

                    }

        position_response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(position_response.status_code, 200)
        self.assertEqual(position_response.context['ajax_request'], True)
        self.assertContains(position_response, 'Zbigniew Adamski')
        self.assertContains(position_response, 'Paweł Testowy')
        self.assertContains(position_response, 'Paweltest Testowyy')
        self.assertNotContains(position_response, 'Waldemar Kiepski')

    def test_should_employee_filter_work_properly(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employees')

        get_data = {'employee_filter': 'ala',

                    }

        response = self.client.get(url, get_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ajax_request'], True)
        self.assertQuerysetEqual(
            response.context['page_employee_list'],
            ['<Employee: Alan Shepard>'])


class ContractExtensionBusinessLogicTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_should_business_logic_1_month_extension_work_properly(self):
        dict = {2: [True, date(2018, 10, 19)],
                3: [True, date(2018, 1, 19)],
                4: [True, date(2017, 2, 27)],
                6: [True, date(2018, 1, 19)],
                12: [True, date(2017, 3, 2)],
                11: [False, None],
                29: [False, None],
                }

        for key in dict.keys():
            from employees.views_business_logic import ContractExtension
            contractExtension = ContractExtension()

            extend_status = dict.get(key)[0]

            self.assertEqual(contractExtension.add_one_month(key), extend_status)
            exp_date = dict.get(key)[1]

            self.assertEqual(contractExtension.exp_date, exp_date)


    def test_should_business_logic_3_month_extension_work_properly(self):
        dict = {2: [True, date(2018, 12, 19)],
                3: [True, date(2018, 3, 19)],
                4: [True, date(2017, 4, 27)],
                6: [True, date(2018, 3, 19)],
                12: [True, date(2017, 5, 2)],
                11: [False, None],
                29: [False, None],
                }

        for key in dict.keys():
            from employees.views_business_logic import ContractExtension
            contractExtension = ContractExtension()

            extend_status = dict.get(key)[0]

            self.assertEqual(contractExtension.add_three_months(key), extend_status)
            exp_date = dict.get(key)[1]

            self.assertEqual(contractExtension.exp_date, exp_date)



# class ContractExtensionViewStatusTests(TestCase):
#     fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']
#
#     # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
#     # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
#     # reason- loading fikstura_cities takes very long time
#
#     def setUp(self):
#         self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
#         zbigniew_adamski = Employee.objects.get(id=3)
#         assert ('Zbigniew Adamski' == str(
#             zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'
#
#     def test_should_business_logic_extension_work_properly(self):
#         dict = {3: True,
#                 2: True,
#                 4: True,
#                 6: True,
#                 12: True,
#                 11: False,
#                 29: False
#                 }
#
#         for key in dict.keys():
#             self.__should_contract_extension_work_properly(key, dict.get(key), 'add_1_month')
#             self.__should_contract_extension_work_properly(key, dict.get(key), 'add_3_month')
#
#     def __should_contract_extension_work_properly(self, id, answer_status, extension):
#
#         kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
#         url = reverse('employee_action')
#
#         get_data = {'extensionLength': extension,
#                     'employeeId': id,
#                     }
#
#         response = self.client.post(url, get_data, **kwargs)
#         self.assertEqual(response.status_code, 200)
#
#         import json
#         dict = json.loads(response.content)
#
#         status = dict[0]
#         name = dict[1]
#         date = dict[2]
#
#         self.assertEqual(status, answer_status)






class ContractExtensionViewCorrectDateTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json
    # reason- loading fikstura_cities takes very long time

    def setUp(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_should_business_logic_extension_work_properly(self):
        dict = {2: [True, '2018-10-19', 'Jakub Czachura'],
                3: [True, '2018-01-19', 'Zbigniew Adamski'],
                4: [True, '2017-02-27', 'Czarny Lodziarz' ],
                6: [True, '2018-01-19', 'Andrzej Strzelba'],
                12: [True, '2017-03-02', 'Ccc Ccc'],
                11: [False, 'null', 'Bbb Bbb'],
                29: [False, 'null', 'Paweł Testowy'],
                }

        for key in dict.keys():
            self.__should_contract_extension_work_properly(key, dict.get(key)[0], dict.get(key)[1], dict.get(key)[2], 'add_1_id')
            # self.__should_contract_extension_work_properly(key, dict.get(key), 'add_3_month')

    def __should_contract_extension_work_properly(self, id, answer_status, expected_date, expected_name, extension):

        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('employee_action')

        get_data = {'extensionLength': extension,
                    'employeeId': id,
                    }

        response = self.client.post(url, get_data, **kwargs)
        self.assertEqual(response.status_code, 200)

        import json
        dict = json.loads(response.content)

        status = dict[0]
        name = dict[1]
        date = dict[2]

        self.assertEqual(status, answer_status)
        self.assertEqual(name, expected_name)
        self.assertIn(expected_date, date)






@skip
class MonthFilterTests(TestCase):
    fixtures = ['fixtures.json']
    c = Client()

    def test_should_hide_unpaid_months_filter_work(self):
        admin_login(self)
        employee = Employee.objects.get(email="czarny@lody.pl")
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url + "?hide_unpaid_months_filter=on")
        self.assertQuerysetEqual(response.context['months'],
                                 ['<Month: March 2017>'])

    def test_should_hide_paid_months_filter_work(self):
        admin_login(self)
        employee = Employee.objects.get(email="czarny@lody.pl")
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url + "?hide_paid_months_filter=on")
        self.assertEqual(len(response.context['months']), 10)

    def test_should_year_filters_work(self):
        admin_login(self)
        employee = Employee.objects.get(email="czarny@lody.pl")
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url + "?2017=on")
        self.assertQuerysetEqual(response.context['months'],
                                 ['<Month: March 2017>', '<Month: February 2017>', '<Month: January 2017>'])
        response = self.c.get(url + "?2018=on")
        self.assertQuerysetEqual(response.context['months'],

                                 ['<Month: January 2018>'])


@skip
class MonthApproveTests(TestCase):
    fixtures = ['fikstura_approve.yaml']

    def test_approve_month_page_should_be_accessible_to_employee(self):
        employee = Employee.objects.get(email='zbigniew@polishlody.com')
        month = Month.objects.filter(employee=employee.id).order_by('id')[0]

        success = self.client.login(username=employee.email, password='codepassword')
        assert success

        url = reverse('month_approve', kwargs={'pk': month.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_approve_month_page_should_be_inaccessible_to_staff(self):
        employee_admin = User.objects.get(email='admin@polishlody.com')
        employee = Employee.objects.get(email='zbigniew@polishlody.com')
        month = Month.objects.filter(employee=employee.id).order_by('id')[0]

        success = self.client.login(username=employee_admin.email, password='codepassword')
        assert success

        url = reverse('month_approve', kwargs={'pk': month.id})
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_approve_month_page_should_be_inaccessible_to_wrong_employee(self):
        employee_1 = Employee.objects.get(email='a.shep@mail.com')
        employee_2 = Employee.objects.get(email='zbigniew@polishlody.com')
        month = Month.objects.filter(employee=employee_2.id).order_by('id')[0]

        success = self.client.login(username=employee_1.email, password='codepassword')
        assert success

        url = reverse('month_approve', kwargs={'pk': month.id})
        response = self.client.get(url)
        # print(url)
        self.assertNotEqual(response.status_code, 200)

    def test_month_approval_status_should_become_false_after_hours_worked_in_month_change_by_staff(self):
        employee_1 = Employee.objects.get(email='z_niewypal@polishlody.com')
        employee_2 = Employee.objects.get(email='zbigniew@polishlody.com')
        month = Month.objects.get(pk=5)

        assert employee_1.is_staff == True
        assert month.month_is_approved == True

        success = self.client.login(username=employee_1.email, password='codepassword')
        assert success

        url = reverse('month_edit', kwargs={'pk': month.id})

        data = {'employee': employee_2.id,
                'salary_is_paid': False,
                'hours_worked_in_this_month': 101,
                'rate_per_hour_this_month': 11,
                'year': 2017,
                'month': 1}

        response_post = self.client.post(url, data=data)
        month.refresh_from_db()

        self.assertEqual(month.month_is_approved, False)

    def test_month_approval_status_should_become_false_after_hours_worked_in_month_and_other_fields_change_by_staff(
            self):
        employee_1 = Employee.objects.get(email='z_niewypal@polishlody.com')
        employee_2 = Employee.objects.get(email='zbigniew@polishlody.com')
        month = Month.objects.get(pk=5)

        assert employee_1.is_staff == True
        assert month.month_is_approved == True

        success = self.client.login(username=employee_1.email, password='codepassword')
        assert success

        url = reverse('month_edit', kwargs={'pk': month.id})

        data = {'employee': employee_2.id,
                'salary_is_paid': False,
                'hours_worked_in_this_month': 101,
                'rate_per_hour_this_month': 12,
                'year': 2018,
                'month': 2}

        response_post = self.client.post(url, data=data)
        month.refresh_from_db()

        self.assertEqual(month.month_is_approved, False)

    def test_month_approval_status_should_remain_true_if_salary_paid_is_true(self):
        employee_1 = Employee.objects.get(email='z_niewypal@polishlody.pl')
        employee_2 = Employee.objects.get(email='zbigniew@polishlody.com')
        month = Month.objects.get(pk=4)

        assert employee_1.is_staff == True
        assert month.month_is_approved == True

        success = self.client.login(username=employee_1.email, password='codepassword')
        assert success

        url = reverse('month_edit', kwargs={'pk': month.id})

        data = {'employee': employee_2.id,
                'salary_is_paid': True,
                'hours_worked_in_this_month': 153,
                'rate_per_hour_this_month': 11,
                'year': 2016,
                'month': 12}

        response_post = self.client.post(url, data=data)
        month.refresh_from_db()

        self.assertEqual(month.month_is_approved, True)


@skip
class CityAutocompleteTests(TestCase):
    fixtures = ['fikstura_approve.yaml', 'fikstura_cities_test.json']

    def test_user_query_should_be_registered_by_view(self):
        print('test')

        employee_1 = Employee.objects.get(email='z_niewypal@polishlody.com')
        assert employee_1.is_staff == True

        success = self.client.login(username=employee_1.email, password='codepassword')
        assert success

        url = reverse('employee_new')

        response = self.client.get(url, query='Wro')

        print(response)

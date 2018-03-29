from django.contrib.auth import get_user_model
from unittest2 import skip

from users.models import MyUser
from django.test import TestCase, Client, RequestFactory
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
        self.assertEqual(len(response.context['all_employee_list']), 1)
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
        self.assertEqual(len(response.context['all_employee_list']), 5)
        self.assertEqual(response.context['orderby'], 'rate_per_hour')


    def test_employee_list_view_should_keep_filters_when_user_returns(self):
     #    test integracyjny
     pass


class EmployeeDetailViewTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # fixtures = ['fikstura_cities','users_myuser.json', 'employees_employee.json']
    # cities deleted manual from fixtury. To test with cities activate upper line and use employees_employee_with_cities.json

    def setUp(self):
        zbigniew_adamski = Employee.objects.get(id=3)
        assert ('Zbigniew Adamski' == str(
            zbigniew_adamski)), 'Zbigniew Adamski should be in fixtures, check if file contains Zbigniew Adamski or problem with loading fixtures'

    def test_employee_detail_view_with_the_existing_record(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        url = reverse_lazy('employee_detail', args=(30,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testowyy Paweltest")
        self.assertContains(response, "pawel@wp.pl")


    def test_employee_message_view_with_the_existing_record(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        url = reverse_lazy('employee_message', args=(47,))
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nie zgadzam sie")

    def test_should_employee_detail_view_show_correct_amount_of_months(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')

        url = reverse_lazy('employee_detail', args=(29,))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['months'],
            ['<Month: February 2018>',
             '<Month: January 2018>', ]
        )

    def test_should_employee_detail_view_be_paginated(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')

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
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')

        url = reverse_lazy('employee_detail', args=(29,))

        from employees.forms import MonthForm
        form = MonthForm({
            'year'                          : '2018',
            'month'                          : '3',
            'salary_is_paid'                : False,
            'hours_worked_in_this_month'    : '150',
            'rate_per_hour_this_month'      : '15',
            'bonuses'                       :   '100',
        })


        self.assertTrue(form.is_valid())
        march2018 = form.save()

        self.assertEqual(march2018.year, 2018)
        self.assertEqual(march2018.month, 3)
        self.assertEqual(march2018.salary_is_paid, False)
        self.assertEqual(march2018.rate_per_hour_this_month, 15)

       





@skip
class EmployeeDetailViewTests_old_version(TestCase):
    fixtures = ['users_myuser.json', ]
    c = Client()

    def test_employee_detail_view_with_the_existing_record(self):
        """
        the detail view of an existing employee should be return status_code 200
        """
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        admin_login(self)
        employee = Employee(first_name='John', last_name='Gamlet', email="gamlet@example.com",
                            contract_start_date=start_date,
                            contract_exp_date=exp_date,
                            )
        employee.save()
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")

    def test_employee_detail_view_with_no_existing_record(self):
        """
        the detail view of a no existing employee should be return status_code 404
        """
        admin_login(self)
        url = reverse_lazy('employee_detail', args=(120215454121,))
        ###
        ### For some reason this test wouldnt work in traditional way (response = self.c.get(url) raised
        ### error 404 and failed test.
        try:
            status_code = self.c.get(url, follow=True)
            print(url)
            print(status_code.content)
        except:
            status_code = 404
        self.assertEqual(status_code, 404)



class EmployeeDetailViewWithGrzesieksFixturesTests(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']







@skip
class EmployeeDetailViewWithGrzesieksFixturesTests_old_version(TestCase):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']
    # fixtures = ['fixtures.json']
    c = Client()

    def test_should_employee_detail_view_show_correct_amount_of_months(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        employee = Employee.objects.create(first_name="Alan",
                                           last_name="Shepard",
                                           email="shepard@mail.com",
                                           contract_start_date=start_date,
                                           contract_exp_date=exp_date
                                           )
        employee.save()
        # admin_login(self)
        first_month = Month(
            month=1,
            year=2016,
            employee=employee,
        )
        another_month = Month(
            month=3,
            year=2016,
            employee=employee,
            salary_is_paid=True,
        )
        another_month.save()
        first_month.save()
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url)
        self.assertQuerysetEqual(
            response.context['months'],
            ['<Month: March 2016>', '<Month: January 2016>']
        )

    def test_should_employee_detail_view_be_paginated(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        employee = Employee.objects.create(first_name="Alan",
                                           last_name="Shepard",
                                           email="shepard@mail.com",
                                           contract_start_date=start_date,
                                           contract_exp_date=exp_date
                                           )
        employee.save()
        # admin_login(self)
        first_month = Month(
            month=1,
            year=2016,
            employee=employee,
        )
        second_month = Month(
            month=3,
            year=2016,
            employee=employee,
            salary_is_paid=True,
        )
        third_month = Month(
            month=5,
            year=2016,
            employee=employee
        )

        third_month.save()
        second_month.save()
        first_month.save()
        url = reverse_lazy('employee_detail', args=(employee.id,)) + "?per_page=2"
        response = self.c.get(url)
        self.assertTrue('2016 May' in str(response.content))
        self.assertTrue('2016 January' not in str(response.content))
        url = reverse_lazy('employee_detail', args=(employee.id,)) + "?page=2&per_page=2"
        response = self.c.get(url)
        self.assertTrue('2016 January' in str(response.content))
        self.assertTrue('2016 May' not in str(response.content))

    def test_should_month_create_view_work(self):
        self.client.login(username='pawel.kisielewicz@codepoets.it', password='codepoets')
        # admin_login(self)
        employee = random.choice(Employee.objects.all())
        url = reverse_lazy('month_new', args=(employee.id,))
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['employee'], employee)
        initial_form_data = response.context['form']
        self.assertTrue('selected="selected">%s<' % (str(employee)) in str(initial_form_data['employee']))
        self.assertTrue('type="number" value="%d" required' % (date.today().year) in str(initial_form_data['year']))
        self.assertTrue('type="number" value="%s" required' %
                        (employee.rate_per_hour) in
                        str(initial_form_data['rate_per_hour_this_month']))


@skip
class EmployeeDeleteViewTests(TestCase):
    fixtures = ['fixtures.json']
    c = Client()

    def test_should_employee_delete_method_work_properly(self):
        admin_login(self)
        start_date = date(2184, 11, 7)
        exp_date = date(2186, 11, 7, )
        emp = Employee(first_name="Alan", last_name="Shepard", email="shepard@mail.com",
                       contract_start_date=start_date,
                       contract_exp_date=exp_date)
        emp.save()
        m = Month(year=2185, month=11, rate_per_hour_this_month=10,
                  hours_worked_in_this_month=300, employee=emp)
        m.save()
        emp_id = emp.id
        response = self.c.get(reverse('employee_delete', args=(emp.id,)), follow=True)
        self.assertTrue('Are you sure you want to delete' in str(response.content))
        post_response = self.c.post(reverse('month_delete', args=(m.id,)), follow=True)
        self.assertRedirects(post_response, reverse('employee_detail', args=(emp.id,)), status_code=302)
        emp.delete()
        response404 = self.c.get(reverse('month_delete', args=(m.id,)), follow=True)
        self.assertTrue('does not exist' in str(response404.content))


@skip
class MonthCreateAndUpdateViewTests(TestCase):
    fixtures = ['fixtures.json']
    c = Client()

    def test_should_month_update_view_work(self):
        admin_login(self)
        month = random.choice(Month.objects.all())
        employee = month.employee  # .__str__()
        year = month.year
        url = reverse_lazy('month_edit', args=(month.id,))
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['month'], month)
        initial_form_data = response.context['form']
        self.assertTrue('selected="selected">%s<' % (employee) in str(initial_form_data['employee']))
        self.assertTrue('type="number" value="%d" required' % (year) in str(initial_form_data['year']))
        self.assertTrue('type="number" value="%s" required' %
                        (month.rate_per_hour_this_month) in
                        str(initial_form_data['rate_per_hour_this_month']))

    def test_should_month_save_method_work_properly(self):
        start_date = date(2184, 11, 7)
        exp_date = date(2186, 11, 7, )
        emp = Employee(first_name="Alan", last_name="Shepard", email="shepard@mail.com",
                       contract_start_date=start_date,
                       contract_exp_date=exp_date)
        emp.save()
        month_date = date(2016, 11, 7)
        m = Month(year=2185, month=11, rate_per_hour_this_month=10,
                  hours_worked_in_this_month=300, employee=emp)
        m.save()
        m2 = Month(year=2186, month=7, rate_per_hour_this_month=10,
                   hours_worked_in_this_month=150, employee=emp, salary_is_paid=True)
        m2.save()
        self.assertEqual(emp.month_set.all().count(), 2)
        mon = Month(year=month_date.year, month=month_date.month, rate_per_hour_this_month=10,
                    hours_worked_in_this_month=300, employee=emp)
        self.assertEqual(m.calculating_salary_for_this_month(), 3000)
        self.assertEqual(m.month_name(), 'November')
        self.assertEqual(m.month_detail(), '2185 November')
        fail_month = Month(year=2185, month=11, rate_per_hour_this_month=10,
                           hours_worked_in_this_month=300, employee=emp)
        self.assertEqual(emp.all_unpaid_salaries(), 3000)
        try:
            fail_month.save()
        except IntegrityError:
            print("Unique together constraint raises IntegrityError as expected.")


@skip
class MonthDeleteViewTests(TestCase):
    fixtures = ['user.json']
    c = Client()

    def test_should_month_delete_method_work_properly(self):
        admin_login(self)
        start_date = date(2184, 11, 7)
        exp_date = date(2186, 11, 7, )
        emp = Employee(first_name="Alan", last_name="Shepard", email="shepard@mail.com",
                       contract_start_date=start_date,
                       contract_exp_date=exp_date)
        emp.save()
        m = Month(year=2185, month=11, rate_per_hour_this_month=10,
                  hours_worked_in_this_month=300, employee=emp)
        m.save()
        m_id = m.id
        response = self.c.get(reverse('month_delete', args=(m_id,)), follow=True)
        self.assertTrue('Are you sure you want to delete' in str(response.content))
        post_response = self.c.post(reverse('month_delete', args=(m.id,)), follow=True)
        self.assertRedirects(post_response, reverse('employee_detail', args=(emp.id,)), status_code=302)
        m.delete()
        response404 = self.c.get(reverse('month_delete', args=(m_id,)), follow=True)
        self.assertTrue('not exist anymore' in str(response404.content))


@skip
class EmployeeFilterTests(TestCase):
    fixtures = ['fixtures.json']
    c = Client()

    def test_should_name_filter_work_properly(self):
        admin_login(self)
        url = reverse_lazy('employees')
        response = self.c.get(url)
        filtered_response = self.c.get(url + "?employee_filter=czarny")
        self.assertQuerysetEqual(
            filtered_response.context['all_employee_list'],
            ['<Employee: Czarny Lodziarz>']
        )
        filtered_response_multiple_results = self.c.get(url + "?employee_filter=w")
        self.assertQuerysetEqual(
            filtered_response_multiple_results.context['all_employee_list'],
            ['<Employee: Jarosław K.>', '<Employee: Waldemar Kiepski>']
        )
        filtered_response_none = self.c.get(url + "?employee_filter=inexistent_potato")
        self.assertQuerysetEqual(
            filtered_response_none.context['all_employee_list'],
            []
        )
        self.assertTrue("No employee meets the search criteria." in str(filtered_response_none.content))

    def test_should_position_filter_work_properly(self):
        admin_login(self)
        url = reverse_lazy('employees')
        position_response = self.c.get(url + "?position_other=on")
        print(position_response)
        self.assertQuerysetEqual(
            position_response.context['all_employee_list'],
            ['<Employee: Waldemar Kiepski>']
        )
        position_response_sale = self.c.get(url + "?position_sale=on")
        self.assertQuerysetEqual(
            position_response_sale.context['all_employee_list'],
            ['<Employee: Jarosław K.>', '<Employee: Mietek Żul>'],
        )
        position_response_production = self.c.get(url + "?position_production=on")
        self.assertQuerysetEqual(
            position_response_production.context['all_employee_list'],
            ['<Employee: Czarny Lodziarz>'],
        )
        position_response_none = self.c.get(url + "?inexistent_position=on")
        self.assertQuerysetEqual(
            position_response_none.context['all_employee_list'],
            ['<Employee: Jarosław K.>', '<Employee: Waldemar Kiepski>', '<Employee: Czarny Lodziarz>',
             '<Employee: Jadzia Pani>', '<Employee: Mietek Żul>']
        )

    def test_should_hide_unpaid_employees_filter_work_properly(self):
        admin_login(self)
        url = reverse_lazy('employees')
        unpaid_response = self.c.get(url + "?hide_zero_salary_months=on")
        self.assertQuerysetEqual(
            unpaid_response.context['all_employee_list'],
            ['<Employee: Jarosław K.>', '<Employee: Waldemar Kiepski>',
             '<Employee: Jadzia Pani>', '<Employee: Mietek Żul>']
        )

    def test_should_hide_paid_employees_filter_work_properly(self):
        admin_login(self)
        url = reverse_lazy('employees')
        unpaid_response = self.c.get(url + "?hide_paid_employees_filter=on")
        self.assertQuerysetEqual(
            unpaid_response.context['all_employee_list'],
            ['<Employee: Czarny Lodziarz>']
        )

    def test_should_multiple_filters_at_a_time_work_properly(self):
        admin_login(self)
        url = reverse_lazy('employees')
        response = self.c.get(url + "?employee_filter=w&position_filter=Sale&position_filter=Other"
                                    "&position_filter=Production&hide_zero_salary_months=on")
        self.assertQuerysetEqual(
            response.context['all_employee_list'],
            ['<Employee: Jarosław K.>', '<Employee: Waldemar Kiepski>']
        )


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

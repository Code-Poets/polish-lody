from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse_lazy
from datetime import datetime, timedelta, date
from .models import Employee, Month, Year

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
        self.assertEqual(e.full_name(), "John Gamlet")

    def test_create_new_employee_with_empty_attributes(self):
        """
        saving employee without all required data should be aborted
        """
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        with self.assertRaises(IntegrityError):
            Employee(first_name=None, last_name=None, email="gamlet.com", contract_start_date=start_date,
            contract_exp_date=exp_date).save()

    fixtures = ['fixtures_user_and_months.json']

    def test_should_calculating_salary_from_all_unpaid_months_work(self):
        employee = Employee.objects.get(first_name='Britney')
        all_months = employee.month_set.all()
        sum_of_all_months = 0
        for mon in all_months:
            rph = mon.rate_per_hour_this_month
            hpm = mon.hours_worked_in_this_month
            sal = (rph * hpm)
            sum_of_all_months += sal
            sum_of_all_months -= mon.how_much_was_paid_to_employee
        self.assertEqual(sum_of_all_months, 1750.00)
        employee = Employee.objects.get(first_name='Czarny')
        all_months = employee.month_set.all()
        sum_of_all_months = 0
        for mon in all_months:
            rph = mon.rate_per_hour_this_month
            hpm = mon.hours_worked_in_this_month
            sal = (rph * hpm)
            sum_of_all_months += sal
            sum_of_all_months -= mon.how_much_was_paid_to_employee
        self.assertEqual(sum_of_all_months, 0)

    def test_should_save_method_create_appropriate_years_and_months_for_single_year(self):
        start_date = date(2016, 3, 1)
        exp_date = date(2016, 11, 1)
        Employee(first_name="Alan", last_name="Shepard", email="asdf@mail.com", contract_start_date=start_date,
                 contract_exp_date=exp_date).save()
        employee = Employee.objects.get(first_name='Alan')
        employee_months = employee.month_set.all()
        employee_years = employee.year_set.all()
        self.assertEqual(employee_months.count(), 9)
        self.assertEqual(employee_months[0].simple_month_name(), 'March')
        self.assertEqual(employee_months[8].simple_month_name(), 'November')
        self.assertEqual(employee_months[2].simple_month_name(), 'May')
        self.assertEqual(employee_years.count(), 1)
        self.assertEqual(employee_years[0].year, '2016')

    def test_should_save_method_create_two_years_and_appropriate_months_for_two_years_of_work(self):
        start_date = date(2183, 2, 1)
        exp_date = date(2184, 11, 1)
        employee = Employee(first_name="Alan", last_name="Shepard", email="asdf@mail.com",
                            contract_start_date=start_date,
                            contract_exp_date=exp_date,
                            rate_per_hour='100'
                            )
        employee.save()
        e = Employee.objects.get(first_name='Alan')
        employee_months = e.month_set.all()
        m = Month.objects.get(employee=e, month='January')
        m.salary_is_paid = True
        m.save()
        employee_years = e.year_set.all()
        self.assertEqual(employee_months.count(), 22)
        self.assertEqual(employee_months[0].simple_month_name(), 'February')
        self.assertEqual(employee_months[8].simple_month_name(), 'October')
        self.assertEqual(employee_months[21].simple_month_name(), 'November')
        self.assertEqual(employee_months[0].month_detail(), '2183 February')
        self.assertTrue(employee_months[11].salary_is_paid) #Checks if month Jan 2184 is paid
        self.assertEqual(employee_years.count(), 2)
        self.assertEqual(employee_years[0].year, '2183')
        self.assertEqual(employee_years[1].year, '2184')
        ### Checks if default rate per hour is assigned for this month
        self.assertEqual(str(employee_months[21].rate_per_hour_this_month), '100.00')


class EmployeeListViewTests(TestCase):

    fixtures = ['user.json',]

    c = Client()

    def test_employee_list_view_with_no_employees(self):
        """
        if no employees exist, an appropritate message should be displayed
        """
        self.c.login(username='manager@polishlody.pl', password='codepassword')
        response = self.c.get(reverse_lazy('employees'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The list of employees is empty")
        self.assertQuerysetEqual(response.context['all_employee_list'], [])

    def test_employee_list_view_with_employees(self):
        """
        all employees from a database should be displayed on the employees page
        """
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        first_employee = Employee(
            first_name='Example', 
            last_name='Example', 
            email='example@example.com',
            contract_start_date=start_date,
            contract_exp_date=exp_date,
        )
        first_employee.save()
        second_employee = Employee(
            first_name='Example2', 
            last_name='Example2', 
            email='example2@example.com',
            contract_start_date=start_date,
            contract_exp_date=exp_date,
        )
        second_employee.save()
        self.c.login(username='manager@polishlody.pl', password='codepassword')
        response = self.c.get(reverse_lazy('employees'))
        self.assertQuerysetEqual(
            response.context['all_employee_list'], 
            ['<Employee: Example Example>', '<Employee: Example2 Example2>']
        )


class EmployeeDetailViewTests(TestCase):

    fixtures = ['user.json',]

    c = Client()

    def test_employee_detail_view_with_the_existing_record(self):
        """
        the detail view of an existing employee should be return status_code 200
        """
        start_date = date.today()
        exp_date = date.today() + timedelta(days=30)
        self.c.login(username='manager@polishlody.pl', password='codepassword')
        employee = Employee(first_name='John', last_name='Gamlet', email="gamlet@example.com",
                            contract_start_date=start_date,
                            contract_exp_date=exp_date,
                            )
        employee.save()
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")

    def test_employee_detail_view_with_no_existing_record(self):
        """
        the detail view of a no existing employee should be return status_code 404
        """
        self.c.login(username='manager@polishlody.pl', password='codepassword')
        url = reverse_lazy('employee_detail', args=(120215454121,))
        response = self.c.get(url)
        self.assertEqual(response.status_code, 404)

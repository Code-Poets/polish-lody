from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse_lazy

from .models import Employee

class EmployeeMethodTests(TestCase):

    def test_full_name_with_valid_employee(self):
        """
        the full_name method should return joined (' ') first_name and last_name
        """
        e = Employee(first_name='John', last_name='Gamlet', email="gamlet@example.com")
        self.assertEqual(e.full_name(), "John Gamlet")

    def test_create_new_employee_with_empty_attributes(self):
        """
        saving employee without all required data should be aborted
        """
        with self.assertRaises(IntegrityError):
            Employee(first_name=None, last_name=None, email="gamlet.com").save()

class EmployeeListViewTests(TestCase):

    c = Client()

    def test_employee_list_view_with_no_employees(self):
        """
        if no employees exist, an appropritate message should be displayed
        """
        response = self.client.get(reverse_lazy('employees'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The list of employees is empty")
        self.assertQuerysetEqual(response.context['all_employee_list'], [])

    def test_employee_list_view_with_employees(self):
        """
        all employees from a database should be displayed on the employees page
        """
        first_employee = Employee(
            first_name='Example', 
            last_name='Example', 
            email='example@example.com'
        ).save()
        second_employee = Employee(
            first_name='Example2', 
            last_name='Example2', 
            email='example2@example.com'
        ).save()
        response = self.client.get(reverse_lazy('employees'))
        self.assertQuerysetEqual(
            response.context['all_employee_list'], 
            ['<Employee: Example>', '<Employee: Example2>']
        )

class EmployeeDetailViewTests(TestCase):

    c = Client()

    def test_employee_detail_view_with_the_existing_record(self):
        """
        the detail view of an existing employee should be return status_code 200
        """
        employee = Employee(first_name='John', last_name='Gamlet', email="gamlet@example.com")
        employee.save()
        url = reverse_lazy('employee_detail', args=(employee.id,))
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")

    def test_employee_detail_view_with_no_existing_record(self):
        """
        the detail view of a no existing employee should be return status_code 404
        """
        url = reverse_lazy('employee_detail', args=(120215454121,))
        response = self.c.get(url)
        self.assertEqual(response.status_code, 404)

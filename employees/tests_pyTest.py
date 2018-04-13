import pytest



#
# from employees import views
#


# class EmployeeDetailViewTests(object):
# from employees.views import EmployeeAction
# from employees.views_business_logic import EmployeeAction


class TestEmployeeAction(object):
    fixtures = ['users_myuser.json', 'employees_employee.json', 'month.json']

    # def test_one(self):
    #     x = "this"
    #     assert 'h' in x
    #
    # def test_two(self):
    #     x = "hello"
    #     assert hasattr(x, 'check')

    @pytest.mark.parametrize("x", [3, 11])
    @pytest.mark.parametrize("y", [True, False])
    @pytest.mark.django_db
    def test_foo(self, x, y):
        # instance = EmployeeAction()

        # add_one_month(5)
        from employees.views_business_logic import ContractExtension
        assert ContractExtension.add_one_month(x) == y




#
#     @pytest.mark.parametrize("x", [0, 1])
#     @pytest.mark.parametrize("y", [2, 3])
#     def test_add_one_month(self, x, y):
#         pass
#
#
#
# #
# #
# #
# import pytest
# @pytest.mark.parametrize("id", [47])
# @pytest.mark.parametrize("message", ["nie zgadzam sie"])
# def test_employee_message_view_with_the_existing_record_param(id, message):
#     pass
# # def test_employee_message_view_with_the_existing_record_param(self, id, message):
# #     url = reverse_lazy('employee_message', args=(id,))
# #     response = self.client.get(url, follow=True)
# #     self.assertEqual(response.status_code, 200)
# #     self.assertContains(response, message)
# #     # assert eval(message in response)
#

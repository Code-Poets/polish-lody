from employees.models import Employee


class ContractExtension:
    name = None
    exp_date = None

    def add_one_month(self, employee_id):
        employee_to_update = Employee.objects.get(pk=employee_id)

        self.name = employee_to_update.first_name + ' ' + employee_to_update.last_name

        old_date = employee_to_update.contract_exp_date
        self.exp_date = old_date

        if old_date is not None:
            day = old_date.day
            old_month = old_date.month
            old_year = old_date.year
        else:
            return False

        new_year = old_year
        new_month = old_month + 1

        if new_month == 13:
            new_month = 1
            new_year = old_year + 1

        import datetime
        new_date = datetime.date(new_year, new_month, day)
        employee_to_update.contract_exp_date = new_date
        employee_to_update.save()

        updated_employee = Employee.objects.get(pk=employee_id)
        updated_date = updated_employee.contract_exp_date

        if ((old_date.day == updated_date.day) and (old_date.month + 1 == updated_date.month) and (
                old_date.year == updated_date.year)):
            self.exp_date = updated_date
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 1) and (
                old_date.year + 1 == updated_date.year)):
            self.exp_date = updated_date
            return True

        else:
            return False

    def add_three_months(self, employee_id):
        employee_to_update = Employee.objects.get(pk=employee_id)

        self.name = employee_to_update.first_name + ' ' + employee_to_update.last_name

        old_date = employee_to_update.contract_exp_date
        self.exp_date = old_date

        if old_date is not None:
            day = old_date.day
            old_month = old_date.month
            old_year = old_date.year
        else:
            return False

        new_year = old_year

        new_month = old_month + 3

        if new_month == 13:
            new_month = 1
            new_year = old_year + 1

        if new_month == 14:
            new_month = 2
            new_year = old_year + 1

        if new_month == 15:
            new_month = 3
            new_year = old_year + 1

        import datetime
        new_date = datetime.date(new_year, new_month, day)
        employee_to_update.contract_exp_date = new_date
        employee_to_update.save()

        updated_employee = Employee.objects.get(pk=employee_id)
        updated_date = updated_employee.contract_exp_date

        if ((old_date.day == updated_date.day) and (old_date.month + 3 == updated_date.month) and (
                old_date.year == updated_date.year)):
            self.exp_date = updated_date
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 1) and (
                old_date.year + 1 == updated_date.year)):
            self.exp_date = updated_date
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 2) and (
                old_date.year + 1 == updated_date.year)):
            self.exp_date = updated_date
            return True

        elif ((old_date.day == updated_date.day) and (updated_date.month == 3) and (
                old_date.year + 1 == updated_date.year)):
            self.exp_date = updated_date
            return True

        else:
            return False

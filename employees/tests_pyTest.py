import time
from datetime import date
import pytest
from employees.utils import is_expiring_contract


class TestUtils(object):

    @pytest.mark.parametrize("input_data,days_to_contract_expires", [
        (date(2020, 5, 10), 750),
        (date(2015, 5, 11), -1075)])
    def test_is_expiring_contract(self, input_data, days_to_contract_expires):
        current_time = time.time()
        days_left = int(current_time / 86400)
        days_correct = 17641-days_left
        days_to_contract_expires = days_to_contract_expires + days_correct

        assert is_expiring_contract(input_data) == days_to_contract_expires

from django.core.exceptions import ValidationError
import time
import re
from django.utils.translation import ugettext_lazy as _

def is_expiring(exp_date):
    if exp_date is not None:
        expiration_date = exp_date
        current_time = time.time()
        expiration_date = int(time.mktime(time.strptime(str(expiration_date), '%Y-%m-%d')))
        days_left = int((expiration_date - current_time) / 86400)
        if 0 <= days_left <= 30:
            return days_left
        elif 0 > days_left:
            return [days_left, days_left * (-1)]


def is_expiring_contract(exp_date):
    if exp_date is not None:
        expiration_date = exp_date
        current_time = time.time()
        expiration_date = int(time.mktime(time.strptime(str(expiration_date), '%Y-%m-%d')))
        days_left = int((expiration_date - current_time) / 86400)
        return days_left


def sanity_check(account_number):
    assert isinstance(account_number, str)

    if account_number.replace(' ', '').isdigit():

        account_number_sans_checksum = account_number.replace(' ', '')[2:]
        original_checksum = int(account_number[0:2])
        new_checksum = 98 - (int(account_number_sans_checksum + '252100') % 97)

        assert new_checksum >= 0

        if new_checksum < 10:
            new_checksum = int('0' + str(new_checksum))

        if original_checksum != new_checksum:
            raise ValidationError(_("The bank account number you entered is invalid"))

    else:

        raise ValidationError(_('Bank account number cannot contain letters'))


def phone_check(phone_number):
    assert isinstance(phone_number, str)

    phone_number_clean = phone_number.replace(' ', '')

    if phone_number_clean.replace('+', '').isdigit():

        if len(phone_number) <= 3:
            phone_number = ''

        else:

            pattern = re.compile('^\+[0-9]{2}[\s][0-9]{3}[\s][0-9]{3}[\s][0-9]{3}$')

            if not pattern.match(phone_number):
                raise ValidationError(_("The phone number you entered is invalid"))

        return phone_number

    else:

        raise ValidationError(_('Phone number cannot contain letters'))


def zip_check(zip_code):
    assert isinstance(zip_code, str)

    if zip_code.replace('-', '').isdigit():

        pattern = re.compile('^[0-9]{2}-[0-9]{3}$')

        if not pattern.match(zip_code):
            raise ValidationError(_("The zip code you entered is invalid"))

    else:
        raise ValidationError(_('Zip code cannot contain letters'))
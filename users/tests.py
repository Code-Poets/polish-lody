from django.test import TestCase
from .models import MyUserManager, MyUser


class MyUserManagerTests(TestCase):

    def setUp(self):
        self.user_manager = MyUserManager()

    def test_invalid_user_without_email(self):
        """
        create_user() without email address should return ValueError
        """
        email = ''
        password = None
        with self.assertRaises(ValueError):
            self.user_manager.create_user(email=email, password=password)

    def test_invalid_superuser_without_email(self):
        """
        create_superuser() without email address should return ValueError
        """
        email = ''
        password = 'password'
        with self.assertRaises(ValueError):
            self.user_manager.create_superuser(email=email, password=password)


class MyUserTest(TestCase):

    def test_get_full_name_should_return_first_name_plus_last_name(self):
        """
        get_full_name() should return first name plus last name
        """
        email = 'example@example.com'
        password = 'password'
        first_name = 'Example'
        last_name = 'User'
        user = MyUser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        full_name = user.get_full_name()
        self.assertEqual(full_name, first_name+" "+last_name)

    def test_get_short_name_should_return_first_name(self):
        """
        get_short_name() should return first name
        """
        email = 'example@example.com'
        password = 'password'
        first_name = 'Example'
        last_name = 'User'
        user = MyUser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        short_name = user.get_short_name()
        self.assertEqual(short_name, first_name)
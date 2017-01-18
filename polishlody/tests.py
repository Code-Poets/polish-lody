from django.test import TestCase
from django.test import Client
from django.core import mail
from django.urls import reverse
from django.contrib import auth


class MyTests(TestCase):
    fixtures = ['polishlody/fixtures/fikstura']

    def test_password_reset_get_view_should_render_password_reset_form(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'registration/password_reset_form.html') 

    def test_password_reset_post_view_should_send_token_via_email_if_user_exists(self):
        assert len(mail.outbox) == 0
        response = self.client.post(reverse('password_reset'),{'email': 'email@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_confirm_get_view_should_render_the_form(self):
        response = self.client.post(reverse('password_reset'),{'email': 'email@example.com'})
        assert response.status_code == 302
        assert 'token' in response.context
        token = response.context['token']
        uid = response.context['uid']

        response = self.client.get(reverse('password_reset_confirm', kwargs={'token':token,'uidb64':uid}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, 'registration/password_reset_confirm.html')

    def test_password_reset_process_should_change_password_and_login_user(self):
        response = self.client.post(reverse('password_reset'),{'email': 'email@example.com'})
        assert response.status_code == 302
        assert 'token' in response.context
        token = response.context['token']
        uid = response.context['uid']

    def test_valid_password_should_allow_user_to_be_logged_in_after_reset(self):
        password = "passwordpassword"
        response_reset = self.client.post(reverse('password_reset'),{'email': 'email@example.com'})
        token = response_reset.context['token']
        uid = response_reset.context['uid']
        response_complete = self.client.post(
            reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid}),
            {
                'new_password1': password, 
                'new_password2': password,
            }
        )
        user = auth.get_user(self.client)
        self.assertEqual(response_complete.status_code, 302)
        self.assertEqual(response_complete._headers["location"], ('Location', reverse('password_reset_complete'))) 
        self.assertEqual(user.is_authenticated(), True)
    def test_invalid_password_should_not_allow_user_to_be_logged_in_after_reset(self): 
        password = "abc"
        response_reset = self.client.post(reverse('password_reset'),{'email': 'email@example.com'})
        token = response_reset.context['token']
        uid = response_reset.context['uid']
        response_complete = self.client.post(
            reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid}),
            {
                'new_password1': password, 
                'new_password2': password,
            }
        )
        user = auth.get_user(self.client)
        self.assertEqual(response_complete.status_code, 200)
        self.assertNotIn("location", response_complete._headers)  
        self.assertEqual(user.is_authenticated(), False) 
    def test_password_mismatch_should_not_allow_user_to_be_logged_in_after_reset(self):
        password = "passwordpassword"
        response_reset = self.client.post(reverse('password_reset'),{'email': 'email@example.com'})
        token = response_reset.context['token']
        uid = response_reset.context['uid']
        response_complete = self.client.post(
            reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid}),
            {
                'new_password1': password, 
                'new_password2': password+"z",
            }
        )
        user = auth.get_user(self.client)
        self.assertEqual(response_complete.status_code, 200)
        self.assertNotIn("location", response_complete._headers)  
        self.assertEqual(user.is_authenticated(), False) 

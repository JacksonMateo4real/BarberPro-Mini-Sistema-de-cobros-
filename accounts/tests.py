from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class LoginTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner1', password='clave12345',
            role='owner', phone_number='000'
        )

    def test_login_with_valid_credentials_redirects_to_owner_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': 'owner1',
            'password': 'clave12345',
        })
        self.assertRedirects(response, reverse('owner_dashboard'))

    def test_login_with_invalid_credentials_shows_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'owner1',
            'password': 'incorrecta',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Credenciales incorrectas")

    def test_logout_requires_login(self):
        response = self.client.get(reverse('logout'))
        self.assertNotEqual(response.status_code, 200)


class RolePermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner1', password='clave12345',
            role='owner', phone_number='000'
        )
        self.barber = User.objects.create_user(
            username='barber1', password='clave12345',
            role='barber', phone_number='111'
        )

    def test_anonymous_user_cannot_access_employee_deletion(self):
        response = self.client.post(
            reverse('owner_delete_employee'),
            {'employee_id': self.barber.id}
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(id=self.barber.id).exists())

    def test_barber_cannot_delete_employees(self):
        self.client.login(username='barber1', password='clave12345')
        response = self.client.post(
            reverse('owner_delete_employee'),
            {'employee_id': self.barber.id}
        )
        self.assertRedirects(response, reverse('barber_dashboard'))
        self.assertTrue(User.objects.filter(id=self.barber.id).exists())

    def test_owner_can_delete_employee(self):
        self.client.login(username='owner1', password='clave12345')
        response = self.client.post(
            reverse('owner_delete_employee'),
            {'employee_id': self.barber.id}
        )
        self.assertRedirects(response, reverse('owner_delete_employee_view'))
        self.assertFalse(User.objects.filter(id=self.barber.id).exists())

    def test_anonymous_user_cannot_view_update_employee_page(self):
        response = self.client.get(reverse('owner_update_employee_view'))
        self.assertNotEqual(response.status_code, 200)

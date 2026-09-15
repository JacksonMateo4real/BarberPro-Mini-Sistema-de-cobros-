from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from sales.models import Sale
from clients.models import Client


class RegisterSaleTests(TestCase):
    def setUp(self):
        self.barber = User.objects.create_user(
            username='barber1', password='clave12345',
            role='barber', phone_number='111'
        )

    def test_anonymous_user_cannot_register_sale(self):
        response = self.client.post(reverse('register_new_sale'), {
            'client': 'Cliente Anonimo',
            'service_type': 'haircut',
            'payment_method': 'cash',
        })
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(Sale.objects.count(), 0)

    def test_logged_in_barber_can_register_sale(self):
        self.client.login(username='barber1', password='clave12345')
        response = self.client.post(reverse('register_new_sale'), {
            'client': 'Juan Perez',
            'service_type': 'haircut',
            'payment_method': 'cash',
        })
        self.assertRedirects(response, reverse('barber_dashboard'))
        self.assertEqual(Sale.objects.count(), 1)

        sale = Sale.objects.first()
        self.assertEqual(sale.user, self.barber)
        self.assertEqual(sale.price, Sale.SERVICE_PRICE['haircut'])
        self.assertEqual(Client.objects.count(), 1)

    def test_registering_sale_reuses_existing_client(self):
        Client.objects.create(full_name='Juan Perez')
        self.client.login(username='barber1', password='clave12345')

        self.client.post(reverse('register_new_sale'), {
            'client': 'Juan Perez',
            'service_type': 'beard',
            'payment_method': 'card',
        })

        self.assertEqual(Client.objects.count(), 1)

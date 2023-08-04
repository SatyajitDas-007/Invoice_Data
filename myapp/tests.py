# myapp/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail
from django.core.management import call_command

class InvoiceAPITestCase(APITestCase):
    # Define the invoice_data attribute with the correct data
    invoice_data = {
        'date': '2023-08-01',
        'invoice_no': 'INV-001',
        'customer_name': 'John Doe',
        'details': [
            {
                'description': 'Item 1',
                'quantity': 2,
                'unit_price': '10.00',
                'price': '20.00',
            },
            {
                'description': 'Item 2',
                'quantity': 3,
                'unit_price': '5.00',
                'price': '15.00',
            },
        ]
    }
    @classmethod
    def setUpClass(cls):
        # Load test data from the db.json fixture before running tests
        call_command('loaddata', 'db.json', verbosity=0)
        super().setUpClass()

    def test_create_invoice(self):
        # Test creating a new invoice using the API
        url = reverse('invoice-list')
        response = self.client.post(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)  # Including the one created in the fixture
        self.assertEqual(InvoiceDetail.objects.count(), 4)  # Including the ones created in the fixture

    def test_get_invoices(self):
        # Test retrieving a list of invoices using the API
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the one created in the fixture should be retrieved

    def test_get_invoice_details(self):
        # Test retrieving details of a specific invoice using the API
        url = reverse('invoice-detail', kwargs={'pk': 1})  # Use the correct primary key of the invoice from the fixture
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_no'], 'INV-001')
        self.assertEqual(len(response.data['details']), 2)

    def test_update_invoice(self):
        # Test updating an existing invoice using the API
        url = reverse('invoice-detail', kwargs={'pk': 1})  # Use the correct primary key of the invoice from the fixture
        data = {
            'date': '2023-08-02',
            'invoice_no': 'INV-002',
            'customer_name': 'Jane Smith',
            'details': [
                {
                    'id': str(1),  # Use the correct primary key of the invoice detail from the fixture
                    'description': 'Updated Item 1',
                    'quantity': 3,
                    'unit_price': '12.00',
                    'price': '36.00',
                },
                {
                    'id': str(2),  # Use the correct primary key of the invoice detail from the fixture
                    'description': 'Updated Item 2',
                    'quantity': 4,
                    'unit_price': '6.00',
                    'price': '24.00',
                },
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invoice = Invoice.objects.get(pk=1)  # Get the updated invoice object from the database
        self.assertEqual(invoice.invoice_no, 'INV-002')
        self.assertEqual(invoice.customer_name, 'Jane Smith')
        self.assertEqual(invoice.details.count(), 2)
        self.assertEqual(invoice.details.first().description, 'Updated Item 1')
        self.assertEqual(invoice.details.first().quantity, 3)
        self.assertEqual(str(invoice.details.first().unit_price), '12.00')  # Convert to string to compare with JSON
        self.assertEqual(str(invoice.details.first().price), '36.00')  # Convert to string to compare with JSON

    def test_delete_invoice(self):
        # Test deleting an existing invoice using the API
        url = reverse('invoice-detail', kwargs={'pk': 1})  # Use the correct primary key of the invoice from the fixture
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(InvoiceDetail.objects.count(), 0)

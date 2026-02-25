from django.test import TestCase
from documents.services import generate_receipt

class DocumentTestCase(TestCase):

    def test_receipt_generation(self):
        file = generate_receipt(payment_id=1)
        self.assertIsNotNone(file)
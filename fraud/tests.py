from django.test import TestCase
from fraud.services import check_fraud

class FraudTestCase(TestCase):

    def test_large_amount_flagged(self):
        score = check_fraud(amount=10000000)
        self.assertIn("risk_score", score)
        self.assertTrue(score["risk_score"] > 0)
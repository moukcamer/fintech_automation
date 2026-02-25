from django.test import TestCase
from ai.services import compute_transaction_ai

class AITestCase(TestCase):

    def test_ai_returns_score(self):
        result = compute_transaction_ai({
            "amount": 5000,
            "country": "CM"
        })

        self.assertIn("risk_score", result)
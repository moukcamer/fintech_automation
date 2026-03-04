from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import date
import random
from finance.models import Customer, Account
from accounting.models import Payment


class Command(BaseCommand):
    help = "Generate demo data for Fintech Automation"

    def handle(self, *args, **kwargs):

        self.stdout.write("🚀 Generating demo data...")

        # ==========================
        # 1️⃣ CLEAN EXISTING DATA
        # ==========================
        Payment.objects.all().delete()
        Account.objects.all().delete()
        Customer.objects.all().delete()

        # ==========================
        # 2️⃣ CREATE CENTRAL ACCOUNT
        # ==========================
        central_account = Account.objects.create(
            account_number="0000",
            account_type="SYSTEM",
            balance=0
        )

        self.stdout.write("✅ Central account created (0000)")

        # ==========================
        # 3️⃣ CREATE CUSTOMERS + ACCOUNTS
        # ==========================
        customers = []
        accounts = []

        for i in range(1, 21):
            customer = Customer.objects.create(
                customer_number=f"CUST-{i:03d}",
                first_name=f"Client{i}",
                last_name="Demo",
                email=f"client{i}@demo.com",
                country="Cameroon",
                city="Douala",
                zip_code="00000",
                birth_date=date(1990, 1, 1),
                created_at=timezone.now()
            )
            customers.append(customer)

            account = Account.objects.create(
                account_number=f"100{i:03d}",
                customer=customer,
                account_type="CUSTOMER",
                balance=0
            )
            accounts.append(account)

        self.stdout.write("✅ 20 customers and accounts created")

        # ==========================
        # 4️⃣ GENERATE PAYMENTS
        # ==========================
        total_transactions = 500

        for _ in range(total_transactions):

            debit_account = random.choice(accounts)
            amount = random.randint(1000, 50000)

            payment = Payment.objects.create(
                debit_account=debit_account,
                credit_account=central_account,
                amount=amount,
                description="Demo Transaction",
                status="PENDING"
            )

            # 🔥 POST TRANSACTION (uses your safe post())
            payment.post()
            

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {total_transactions} transactions successfully posted"
            )
        )

        self.stdout.write(
            self.style.SUCCESS("🎉 Demo data generation complete")
        )
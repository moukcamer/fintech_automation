import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from finance.models import Transaction, Account, Customer


class Command(BaseCommand):
    help = "Import transactions from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **options):

        csv_file_path = options["csv_file"]

        self.stdout.write("📥 Importation en cours...")

        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # ============================
                # 1. ACCOUNT
                # ============================
                account_name = row["account"].strip()

                account, _ = Account.objects.get_or_create(
                    name=account_name
                )

                # ============================
                # 2. CUSTOMER
                # ============================
                customer = None
                if row.get("customer"):
                    customer_name = row["customer"].strip()
                    customer, _ = Customer.objects.get_or_create(
                        name=customer_name
                    )

                # ============================
                # 3. TRANSACTION
                # ============================
                Transaction.objects.create(
                    date=parse_date(row["date"]),
                    amount=Decimal(row["amount"]),
                    transaction_type=row["transaction_type"],
                    status=row.get("status", "PAID"),
                    description=row.get("description", ""),
                    account=account,
                    customer=customer
                )

        self.stdout.write(
            self.style.SUCCESS("✅ Import CSV terminé avec succès")
        )

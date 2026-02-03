import csv
from django.core.management.base import BaseCommand
from finance.models import Transaction, Account
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = "Import transactions from transaction.csv"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        created, ignored = 0, 0
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    account = Account.objects.get(
                        account_number=row["account_number"]
                    )
                except Account.DoesNotExist:
                    ignored += 1
                    continue

                Transaction.objects.create(
                    transaction_ref=row["transaction_ref"],
                    account=account,
                    transaction_date=parse_datetime(row["transaction_date"]),
                    amount=row["amount"],
                    currency=row["currency"],
                    transaction_type=row["transaction_type"],
                    description=row.get("description"),
                    channel=row.get("channel"),
                    country=row.get("country"),
                )

                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé — transactions créées: {created}, ignorées: {ignored}"
            )
        )

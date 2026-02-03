import csv
from django.core.management.base import BaseCommand
from finance.models import Account, Customer
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    help = "Import accounts from account.csv"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        created, ignored = 0, 0
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    customer = Customer.objects.get(
                        customer_number=row["customer_number"]
                    )
                except Customer.DoesNotExist:
                    ignored += 1
                    continue

                account, is_created = Account.objects.get_or_create(
                    account_number=row["account_number"],
                    defaults={
                        "customer": customer,
                        "account_type": row["account_type"],
                        "currency": row["currency"].strip(),
                        "balance": row["balance"],
                        "open_date": parse_date(row["open_date"]),
                        "status": row["status"],
                    },
                )

                if is_created:
                    created += 1
                else:
                    ignored += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé — comptes créés: {created}, ignorés: {ignored}"
            )
        )

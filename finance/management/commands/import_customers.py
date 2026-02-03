import csv
from django.core.management.base import BaseCommand
from finance.models import Customer
from django.utils.dateparse import parse_date, parse_datetime


class Command(BaseCommand):
    help = "Import customers from customer.csv"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        created, ignored = 0, 0
        csv_file = kwargs["csv_file"]

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                customer, is_created = Customer.objects.get_or_create(
                    customer_number=row["customer_number"],
                    defaults={
                        "first_name": row["first_name"],
                        "last_name": row["last_name"],
                        "email": row.get("email"),
                        "country": row.get("country", "").strip(),
                        "city": row.get("city"),
                        "zip_code": row.get("zip_code"),
                        "birth_date": parse_date(row.get("birth_date")),
                        "created_at": parse_datetime(row.get("created_at")),
                    },
                )

                if is_created:
                    created += 1
                else:
                    ignored += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé — clients créés: {created}, ignorés: {ignored}"
            )
        )


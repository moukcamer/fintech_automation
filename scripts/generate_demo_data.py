import random
import string
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from accounting.bootstrap import create_chart_of_accounts, create_journals
from finance.models import Customer, Account, Transaction, Invoice, Payment, Company

# ---------------- CONFIG ----------------
NB_COMPANIES = 5
NB_CUSTOMERS = 120
NB_ACCOUNTS = 40
NB_TRANSACTIONS = 8000
NB_FRAUD = 300
NB_ERRORS = 500

CURRENCIES = ["XAF", "EUR", "USD"]
CHANNELS = ["MOBILE", "WEB", "POS", "BANK"]
COUNTRIES = ["Cameroun", "France", "Nigeria", "Kenya"]
ACCOUNT_TYPES = ["CURRENT", "SAVING", "BUSINESS"]

START_DATE = timezone.now() - timedelta(days=365)

def reset_database():
    print("Cleaning old data...")

    Payment.objects.all().delete()
    Invoice.objects.all().delete()
    Transaction.objects.all().delete()
    Account.objects.all().delete()
    Customer.objects.all().delete()
    Company.objects.all().delete()

    print("Database cleaned")

from django.db import connection

def reset_sqlite_sequences():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence")

    

# ---------------- UTILS ----------------
def rand_ref(prefix="TX"):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def rand_date():
    return START_DATE + timedelta(days=random.randint(0, 365), seconds=random.randint(0, 86400))

def rand_amount():
    return Decimal(random.randint(2000, 900000))

# ---------------- COMPANIES ----------------
def create_companies():
    companies = []
    for i in range(NB_COMPANIES):
        c = Company.objects.create(name=f"Company_{i}")
        companies.append(c)
    print("Companies OK")
    return companies

# ---------------- CUSTOMERS ----------------
def create_customers():
    customers = []
    for i in range(NB_CUSTOMERS):
        c = Customer.objects.create(
            customer_number=f"CUST{i:05}",
            first_name=f"Name{i}",
            last_name=f"Surname{i}",
            email=f"client{i}@mail.com",   # ← CORRIGÉ
            country=random.choice(COUNTRIES),
            city="Douala",
            zip_code=str(1000 + i),       # ← évite collisions
            birth_date=datetime(1995,1,1).date(),
            created_at=timezone.now()
        )
        customers.append(c)
    print("Customers OK")
    return customers



# ---------------- ACCOUNTS ----------------
def create_accounts(customers):
    accounts = []
    for i in range(NB_ACCOUNTS):
        acc = Account.objects.create(
            account_number=f"ACC{i:05}",
            customer=random.choice(customers),
            account_type=random.choice(ACCOUNT_TYPES),
            currency=random.choice(CURRENCIES),
            balance=Decimal(0),
            open_date="2023-01-01",
            status="ACTIVE",
            credit_score=random.randint(20, 90)
        )
        accounts.append(acc)
    print("Accounts OK")
    return accounts

# ---------------- TRANSACTIONS ----------------
def create_transactions(accounts):
    print("Creating normal transactions...")
    for _ in range(NB_TRANSACTIONS):
        Transaction.objects.create(
            transaction_ref=rand_ref(),
            account=random.choice(accounts),
            transaction_date=rand_date(),
            amount=rand_amount(),
            currency=random.choice(CURRENCIES),
            transaction_type=random.choice(["IN","OUT"]),
            description="Normal transaction",
            channel=random.choice(CHANNELS),
            country=random.choice(COUNTRIES),
            fraud_score=random.uniform(0, 0.3),
            is_fraud=False
        )
    print("Normal transactions OK")

# ---------------- FRAUD ----------------
def create_frauds(accounts):
    print("Injecting frauds...")
    for _ in range(NB_FRAUD):
        Transaction.objects.create(
            transaction_ref=rand_ref("FRD"),
            account=random.choice(accounts),
            transaction_date=rand_date(),
            amount=Decimal(random.choice([499999, 899999, 999999])),
            currency="XAF",
            transaction_type="OUT",
            description="Suspicious large withdrawal",
            channel=random.choice(CHANNELS),
            country=random.choice(["Nigeria","Kenya","Ghana"]),
            fraud_score=random.uniform(0.8, 0.99),
            is_fraud=True
        )
    print("Frauds OK")

# ---------------- DIRTY DATA ----------------
def create_dirty_data(accounts):
    print("Injecting bad data...")
    for _ in range(NB_ERRORS):
        Transaction.objects.create(
            transaction_ref=rand_ref("ERR"),
            account=random.choice(accounts),
            transaction_date=rand_date(),
            amount=Decimal(random.choice([-5000, 0, 999999999])),
            currency="XAF",
            transaction_type=random.choice(["IN","OUT"]),
            description="Corrupted data",
            channel="UNKNOWN",
            country="UNKNOWN",
            fraud_score=None,
            is_fraud=False
        )
    print("Dirty data OK")

# ---------------- INVOICES & PAYMENTS ----------------
def create_billing(customers, accounts):
    print("Creating invoices/payments...")
    for _ in range(200):
        inv = Invoice.objects.create(
            customer=random.choice(customers),
            amount=Decimal(random.randint(10000, 500000)),
            status=random.choice(["PENDING","PAID"])
        )
        Payment.objects.create(
            invoice=inv,
            account=random.choice(accounts),
            payment_type=random.choice(["IN","OUT"]),
            amount=inv.amount
        )
    print("Billing OK")

# ---------------- RUN ----------------
def run():
    reset_database()
    reset_sqlite_sequences()

    create_chart_of_accounts()
    create_journals()   # ← AJOUT CRITIQUE

    companies = create_companies()
    customers = create_customers()
    accounts = create_accounts(customers)
    create_transactions(accounts)
    create_frauds(accounts)
    create_dirty_data(accounts)
    create_billing(customers, accounts)

    print("\nBASE ERP FINTECH COMPLETE")
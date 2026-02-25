import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Transaction, Account
from datetime import datetime

# ===============================
# ETAPE 1 : UPLOAD + PREVIEW
# ===============================
def import_transactions(request):

    if request.method == "POST" and request.FILES.get("file"):

        file = request.FILES["file"]

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # normaliser colonnes
        df.columns = [c.lower().strip() for c in df.columns]

        required = ["date", "amount", "type", "account_number"]
        missing = [c for c in required if c not in df.columns]

        if missing:
            return render(request, "finance/import.html", {
                "form": UploadFileForm(),
                "error": f"Colonnes manquantes: {', '.join(missing)}"
            })

        # convertir en dictionnaire pour session
        request.session["import_data"] = df.to_dict("records")

        preview = df.head(20).to_dict("records")

        return render(request, "finance/preview.html", {
            "preview": preview,
            "columns": df.columns
        })

    return render(request, "finance/import.html", {"form": UploadFileForm()})


# ===============================
# ETAPE 2 : CONFIRM IMPORT
# ===============================
from django.db.models import Q
from datetime import datetime

def confirm_import(request):

    data = request.session.get("import_data")

    if not data:
        return redirect("import_transactions")

    created = 0
    duplicates = 0

    for row in data:

        account, _ = Account.objects.get_or_create(
            account_number=row["account_number"]
        )

        tx_date = datetime.strptime(str(row["date"]), "%Y-%m-%d")

        # 🔎 RECHERCHE DOUBLON
        exists = Transaction.objects.filter(
            account=account,
            amount=row["amount"],
            transaction_type=row["type"],
            transaction_date=tx_date
        ).exists()

        if exists:
            duplicates += 1
            continue

        Transaction.objects.create(
            account=account,
            amount=row["amount"],
            transaction_type=row["type"],
            description=row.get("description", ""),
            transaction_date=tx_date
        )

        created += 1

    del request.session["import_data"]

    return render(request, "finance/success.html", {
        "created": created,
        "duplicates": duplicates
    })

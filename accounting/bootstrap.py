from accounting.models import Account, Journal

def create_chart_of_accounts():
    accounts = [
        ("101", "Caisse"),
        ("102", "Banque"),
        ("201", "Clients"),
        ("401", "Fournisseurs"),
        ("601", "Charges"),
        ("701", "Produits"),
    ]

    for code, name in accounts:
        Account.objects.get_or_create(
            code=code,
            defaults={"name": name}
        )

    print("Plan comptable initialisé")


def create_journals():
    journals = [
        ("CAI", "Journal de Caisse"),
        ("BNQ", "Journal de Banque"),
        ("VTE", "Journal des Ventes"),
        ("ACH", "Journal des Achats"),
        ("OD", "Opérations Diverses"),
    ]

    for code, name in journals:
        Journal.objects.get_or_create(
            code=code,
            defaults={"name": name}
        )

    print("Journaux comptables initialisés")


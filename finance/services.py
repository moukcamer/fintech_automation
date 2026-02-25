def post_transaction(payment):
    """
    Création automatique de l'écriture comptable double
    Débit / Crédit après paiement
    """

    if not payment.account:
        return

    account = payment.account

    # Exemple logique comptable simple
    if payment.payment_type == "IN":
        account.balance += payment.amount
    else:
        account.balance -= payment.amount

    account.save(update_fields=["balance"])



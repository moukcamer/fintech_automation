from datetime import datetime

def transform_payment(row):
    return {
        "amount": float(row["amount"]),
        "payment_type": "IN" if row["type"] == "credit" else "OUT",
        "created_at": datetime.strptime(row["date"], "%Y-%m-%d"),
        "description": row.get("description", "")
    }

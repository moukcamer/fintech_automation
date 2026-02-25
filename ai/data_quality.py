import pandas as pd
import numpy as np
from datetime import datetime

def clean_amount(val):
    if pd.isna(val):
        return None
    val = str(val).replace("FCFA","").replace(" ","").replace(",","")
    try:
        return float(val)
    except:
        return None


def normalize_type(val):
    if not val:
        return None

    val = str(val).upper()

    mapping = {
        "CREDIT":"IN",
        "DEPOT":"IN",
        "IN":"IN",
        "ENTREE":"IN",
        "DEBIT":"OUT",
        "RETRAIT":"OUT",
        "SORTIE":"OUT",
        "OUT":"OUT"
    }
    return mapping.get(val, None)


def parse_date(val):
    formats = ["%Y-%m-%d","%d/%m/%Y","%d-%m-%Y","%m/%d/%Y"]
    for f in formats:
        try:
            return datetime.strptime(str(val),f).date()
        except:
            pass
    return None


def quality_score(df):

    total = len(df)
    if total == 0:
        return 0, {}

    issues = {
        "missing_account": df["account_number"].isna().sum(),
        "invalid_amount": df["amount"].isna().sum(),
        "invalid_type": df["type"].isna().sum(),
        "invalid_date": df["date"].isna().sum(),
        "zero_amount": (df["amount"]==0).sum(),
        "future_date": (df["date"]>datetime.now().date()).sum()
    }

    errors = sum(issues.values())

    score = max(0, 100 - int((errors/total)*100))

    return score, issues


def clean_dataframe(df):

    df["amount"] = df["amount"].apply(clean_amount)
    df["type"] = df["type"].apply(normalize_type)
    df["date"] = df["date"].apply(parse_date)

    # corriger montant négatif
    df.loc[(df["amount"]<0) & (df["type"]=="OUT"),"amount"] *= -1

    # supprimer lignes invalides critiques
    df = df.dropna(subset=["account_number","amount","type","date"])

    # supprimer montant zero
    df = df[df["amount"]>0]

    return df
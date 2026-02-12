def compute_risk_score(account_id):
    # ⚠️ logique simplifiée
    score = 72

    return {
        "score": score,
        "level": "HIGH" if score > 70 else "LOW",
        "explanation": "Volume de transactions élevé et irrégulier"
    }

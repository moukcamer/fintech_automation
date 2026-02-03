def generate_recommendation(metrics):
    if metrics["net_result"] < 0:
        return (
            "⚠️ Risque financier détecté. "
            "Il est recommandé de réduire les charges non critiques "
            "et d’accélérer le recouvrement des créances."
        )

    if metrics["cash_balance"] < metrics["expenses_30d"]:
        return (
            "💡 Trésorerie sous tension. "
            "Prévoir une ligne de financement court terme."
        )

    return (
        "✅ Situation financière saine. "
        "Opportunité d’investissement ou d’expansion à court terme."
    )

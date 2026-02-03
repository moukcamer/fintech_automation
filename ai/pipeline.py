#ai/pipelines.py

def run_ai_pipeline(df, kpis):
    from ai.data_prep.cleaning import clean_transactions
    from ai.data_prep.features import add_time_features
    from ai.automl.models import get_models
    from ai.automl.selector import select_best_model
    from ai.explainability.insights import explain_forecast
    from ai.genai.recommendations import generate_recommendation

    df = clean_transactions(df)
    df = add_time_features(df)

    X = df[["rolling_7", "rolling_30", "weekday"]].fillna(0)
    y = df["amount_clean"]

    (model_name, model), score = select_best_model(X, y, get_models())

    forecast = model.predict(X.tail(30))
    explanation = explain_forecast(y.tail(30).tolist(), forecast.tolist())
    recommendation = generate_recommendation(kpis)

    volatility = df["amount_clean"].pct_change().std()

    risk_score = compute_risk_score(
        kpis["net_result"],
        kpis["cash_balance"],
        volatility
    )


    return {
        "model_used": model_name,
        "error": score,
        "forecast": forecast.tolist(),
        "explanation": explanation,
        "recommendation": recommendation,
        "risk_score": risk_score,

    }

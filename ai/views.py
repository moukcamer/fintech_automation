# ai/views.py

from django.http import JsonResponse
from finance.models import Transaction
from ai.services.features import build_features
from ai.services.anomaly import detect_anomalies
from ai.services.forecast import build_cashflow_dataframe, forecast_cashflow
import pandas as pd
from ai.pipeline import run_ai_pipeline
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def ai_report_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="finoptiai_report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>Rapport IA – FinOptiAI</b>", styles["Title"]))
    elements.append(Paragraph("Analyse financière intelligente", styles["Normal"]))

    elements.append(Paragraph(
        f"Score de risque : {request.GET.get('risk', 'N/A')}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        request.GET.get("recommendation", ""),
        styles["Normal"]
    ))

    doc.build(elements)
    return response


def cashflow_forecast(request):
    """
    Prévision simple du cashflow mensuel
    (base IA / prêt pour AutoML plus tard)
    """

    data = (
        Transaction.objects
        .filter(status="completed")
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(cashflow=Sum("amount"))
        .order_by("month")
    )

    labels = []
    values = []

    for row in data:
        labels.append(row["month"].strftime("%Y-%m"))
        values.append(float(row["cashflow"]))

    return JsonResponse({
        "labels": labels,
        "values": values,
        "model": "Baseline Time Series (ready for AutoML)"
    })



def anomaly_detection(request):
    qs = Transaction.objects.filter(status="completed")

    df = build_features(qs)

    if df.empty:
        return JsonResponse({"message": "Aucune donnée"}, status=200)

    result = detect_anomalies(df)
 
    anomalies_count = int((result["anomaly"] == -1).sum())

    return JsonResponse({
        "total_transactions": len(result),
        "anomalies_detected": anomalies_count,
        "anomaly_rate": round(anomalies_count / len(result) * 100, 2)
    })



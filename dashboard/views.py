from django.shortcuts import render
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from datetime import datetime
import pandas as pd
import json
import matplotlib.pyplot as plt
import io
import os
from ai.copilot import financial_copilot
from ai.copilot_insights import auto_financial_insight
from ai.assistant import financial_copilot
from ai.features import build_features
from ai.risk_engine import compute_risk
from ai.insights import generate_insight
from ai.scoring import compute_client_score
from ai.narration import generate_narrative

from finance.models import Account, Transaction

from ml.forecast import financial_forecast as ml_forecast
from ai.forecast import financial_forecast as ai_forecast


# =============================================
# DASHBOARD PRINCIPAL
# =============================================
@login_required(login_url="/login/")
@cache_page(60 * 5)
def dashboard(request):

    # ------------------------
    # 1️⃣ Queryset + filtres
    # ------------------------
    queryset = Transaction.objects.select_related("account").all()

    date_start = request.GET.get("date_start", "").strip()
    date_end = request.GET.get("date_end", "").strip()
    trans_type = request.GET.get("transaction_type", "").strip()
    account_id = request.GET.get("account", "").strip()

    if date_start:
        try:
            dt_start = datetime.strptime(date_start, "%Y-%m-%d")
            queryset = queryset.filter(transaction_date__date__gte=dt_start)
        except:
            pass

    if date_end:
        try:
            dt_end = datetime.strptime(date_end, "%Y-%m-%d")
            queryset = queryset.filter(transaction_date__date__lte=dt_end)
        except:
            pass

    if trans_type in ["IN", "OUT"]:
        queryset = queryset.filter(transaction_type=trans_type)

    if account_id.isdigit():
        queryset = queryset.filter(account_id=int(account_id))

    # ------------------------
    # 2️⃣ KPIs
    # ------------------------
    total_transactions = queryset.count()
    total_amount = float(queryset.aggregate(total=Sum("amount"))["total"] or 0)
    total_income = float(queryset.filter(amount__gt=0).aggregate(total=Sum("amount"))["total"] or 0)
    total_expenses = float(queryset.filter(amount__lt=0).aggregate(total=Sum("amount"))["total"] or 0)
    net_balance = total_income + total_expenses
    total_accounts = Account.objects.count()
    fraud_transactions = queryset.filter(is_fraud=True).count()

    fraud_rate = 0
    if total_transactions > 0:
        fraud_rate = round((fraud_transactions / total_transactions) * 100, 2)

    kpis_ia = {
        "net_balance": net_balance,
        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
    }


    # ------------------------
    # 3️⃣ Graphiques
    # ------------------------
    # Evolution quotidienne
    daily_qs = (
        queryset.annotate(day=TruncDate("transaction_date"))
        .values("day")
        .annotate(
            total_credit=Sum("amount", filter=Q(amount__gt=0)),
            total_debit=Sum("amount", filter=Q(amount__lt=0)),
        )
        .order_by("day")
    )
    evolution_labels = [e["day"].strftime("%d/%m/%Y") for e in daily_qs if e["day"]]
    evolution_data = [float((e["total_credit"] or 0) + (e["total_debit"] or 0)) for e in daily_qs if e["day"]]

    # Evolution mensuelle
    monthly_qs = (
        queryset.annotate(month=TruncMonth("transaction_date"))
        .values("month")
        .annotate(
            total_credit=Sum("amount", filter=Q(amount__gt=0)),
            total_debit=Sum("amount", filter=Q(amount__lt=0)),
        )
        .order_by("month")
    )
    monthly_labels = [e["month"].strftime("%b %Y") for e in monthly_qs if e["month"]]
    monthly_data = [float((e["total_credit"] or 0) + (e["total_debit"] or 0)) for e in monthly_qs if e["month"]]
    forecast_values = ai_forecast(monthly_data, periods=3)
    forecast_labels = ["Prévision 1", "Prévision 2", "Prévision 3"]

    # Répartition par type
    type_qs = queryset.values("transaction_type").annotate(total=Sum("amount")).order_by("-total")
    type_labels = [e["transaction_type"] for e in type_qs]
    type_data = [float(e["total"] or 0) for e in type_qs]

    # comptes actifs

    top_accounts_qs = (
        queryset
        .values("account__account_number")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:5]
    )

    top_accounts_labels = [e["account__account_number"] for e in top_accounts_qs]
    top_accounts_data = [float(e["total"] or 0) for e in top_accounts_qs]


    # ------------------------
    # Graphiques prévision
    # ------------------------
    # Prévision ML
    ml_forecast_values = ml_forecast(monthly_data, periods=3)
    ml_forecast_labels = ["Prévision ML 1", "Prévision ML 2", "Prévision ML 3"]

    # Prévision IA
    ai_forecast_values = ai_forecast(monthly_data, periods=3)
    ai_forecast_labels = ["Prévision IA 1", "Prévision IA 2", "Prévision IA 3"]


    # ------------------------
    # 4️⃣ Analyse IA + Narration
    # ------------------------
    ai_result = {
        "score": 50,
        "alerts": [],
        "text": "Aucune donnée suffisante",
        "model_used": None,
    }
    narrative_text = "Narration indisponible."

    if queryset.exists():
        try:
            df = pd.DataFrame(list(
                queryset.values(
                    "amount",
                    "transaction_type",
                    "account_id",
                    "account__account_number",
                    "transaction_date"
                ).order_by("transaction_date")
            ))
            df.rename(columns={"transaction_date":"date", "account__account_number":"account_number"}, inplace=True)
            df = build_features(df)
            risk = compute_risk(df)
            if not isinstance(risk, dict):
                risk = {"risk_score":50, "alerts":[]}
            if not isinstance(risk.get("alerts"), list):
                risk["alerts"] = []

            kpis_ia = {"net_balance": net_balance, "total_transactions": total_transactions, "total_amount": total_amount}
            insight_text = generate_insight(kpis=kpis_ia, risk=risk)
            narrative_text = generate_narrative(kpis=kpis_ia, 
                                                risk=risk,
                                                 monthly_data=monthly_data, 
                                                 evolution_data=evolution_data,
                                                 fraud_transactions=fraud_transactions
                                                 )

            ai_result.update({
                "score": risk.get("risk_score",50),
                "alerts": risk.get("alerts",[]),
                "text": insight_text or "Activité normale détectée",
                "model_used": "Analyse 2026 v2"
            })
        except Exception as e:
            ai_result["text"] = f"Erreur analyse IA : {str(e)}"
            narrative_text = "Erreur génération narration."

    # ------------------------
    # 5️⃣ Dernières transactions
    # ------------------------
    transactions = queryset.select_related("account").order_by("-transaction_date")[:20]

    # ------------------------
    # 6 Fraud v Normal
    # ------------------------

    fraud_labels = ["Normal", "Fraude"]

    fraud_data = [
        queryset.filter(is_fraud=False).count(),
        queryset.filter(is_fraud=True).count(),
    ]
    
    # ------------------------
    # 7 Fraud v Normal
    # -----------------------

    fraud_transactions = queryset.filter(is_fraud=True).count()

    # ------------------------
    #  Table des transactions suspectes
    # ------------------------

    fraud_list = queryset.filter(is_fraud=True).order_by("-fraud_probability")[:10]
   

    # ------------------------
    # Gestion de l'Assistant IA
    # ------------------------
    question = request.GET.get('question', '').strip()
    context_assistant = None

    if question:
        q = question.lower()
        # Résultat net
        if "résultat net" in q or "solde net" in q:
            total_income = Transaction.objects.filter(transaction_type="IN").aggregate(total=Sum('amount'))['total'] or 0
            total_expenses = Transaction.objects.filter(transaction_type="OUT").aggregate(total=Sum('amount'))['total'] or 0
            net_balance = total_income - total_expenses
            context_assistant = f"✅ Votre résultat net est de {net_balance:,} XAF"

        # Total revenus
        elif "revenus" in q or "total revenus" in q:
            total_income = Transaction.objects.filter(transaction_type="IN").aggregate(total=Sum('amount'))['total'] or 0
            context_assistant = f"💰 Le total des revenus est de {total_income:,} XAF"

        # Total dépenses
        elif "dépenses" in q or "total dépenses" in q:
            total_expenses = Transaction.objects.filter(transaction_type="OUT").aggregate(total=Sum('amount'))['total'] or 0
            context_assistant = f"📉 Le total des dépenses est de {total_expenses:,} XAF"

        # Transactions suspectes
        elif "transactions suspectes" in q or "fraude" in q:
            fraud_count = Transaction.objects.filter(is_fraud=True).count()
            context_assistant = f"🚨 Il y a actuellement {fraud_count} transactions suspectes."

        # Solde d’un compte précis
        elif "solde compte" in q:
            import re
            match = re.search(r'\d+', q)  # extraire l’ID du compte
            if match:
                account_id = int(match.group())
                income = Transaction.objects.filter(account__id=account_id, transaction_type="IN").aggregate(total=Sum('amount'))['total'] or 0
                expenses = Transaction.objects.filter(account__id=account_id, transaction_type="OUT").aggregate(total=Sum('amount'))['total'] or 0
                balance = income - expenses
                context_assistant = f"💳 Le solde du compte {account_id} est de {balance:,} XAF"
            else:
                context_assistant = "⚠️ Veuillez préciser l’ID du compte dans votre question."

        else:
            context_assistant = "❓ Désolé, je n'ai pas compris votre question. Essayez des termes comme 'résultat net', 'revenus', 'dépenses', 'transactions suspectes' ou 'solde compte <ID>'."

    # ------------------------
    # Autres variables du dashboard
    # ------------------------
    transactions = Transaction.objects.all().order_by('-transaction_date')[:50]
    fraud_list = Transaction.objects.filter(is_fraud=True).order_by('-fraud_probability')[:10]

    #------------------------
    # 8 copilot
    #------------------------

    if question and queryset.exists():
        try:
            df_assistant = pd.DataFrame(list(
            queryset.values(
                "amount",
                "account__account_number"
            )
        ))
            
            df_assistant.rename(
            columns={"account__account_number":"account_number"},
            inplace=True
            )
            
            kpis_assistant = {
            "net_balance": net_balance,
            "total_transactions": total_transactions,
            "total_income": total_income,
            "total_expenses": total_expenses
            }
            assistant_answer = financial_copilot(
            question,
            df_assistant,
            kpis_assistant,
            monthly_data,
            risk
            )
        except Exception as e:
            assistant_answer = f"Erreur assistant : {str(e)}"
    
    #------------------------------
    # 9 copilot_insights
    # -----------------------------

    auto_insights = auto_financial_insight(
        kpis_ia,
        monthly_data,
        type_data,
        risk
    )     

    #-------------------------------
    # 12 Scoring
    # ------------------------------
    
    client_score = compute_client_score(df)
       

    # ------------------------
    # 8 Contexte
    # ------------------------

    context = {
    "total_transactions": total_transactions,
    "total_amount": total_amount,
    "total_income": total_income,
    "total_expenses": total_expenses,
    "net_balance": net_balance,
    "total_accounts": total_accounts,
    "ai": ai_result,
    "narrative_text": narrative_text,
    "chart_evolution": {"labels": json.dumps(evolution_labels), "data": json.dumps(evolution_data)},
    "chart_monthly": {"labels": json.dumps(monthly_labels), "data": json.dumps(monthly_data)},
    "chart_types": {"labels": json.dumps(type_labels), "data": json.dumps(type_data)},
    "chart_accounts": {"labels": json.dumps(top_accounts_labels), "data": json.dumps(top_accounts_data)},
    "chart_fraud": {"labels": json.dumps(fraud_labels), "data": json.dumps(fraud_data)},
    "chart_forecast": {"labels": json.dumps(forecast_labels), "data": json.dumps(forecast_values)},
    "fraud_transactions": fraud_transactions,
    "fraud_rate": fraud_rate,
    "fraud_list": fraud_list,
    "filters": {"date_start": date_start, "date_end": date_end, "transaction_type": trans_type, "account_id": account_id},
    "transactions": transactions,
    "context_assistant": context_assistant,
    "question": question,
    "auto_insights": auto_insights,
    "client_score": client_score,
    "chart_forecast_ml": {"labels": json.dumps(ml_forecast_labels),"data": json.dumps(ml_forecast_values),},
    "chart_forecast_ai": {"labels": json.dumps(ai_forecast_labels),"data": json.dumps(ai_forecast_values),},

}
    return render(request, "dashboard/dashboard.html", context)

# =============================================
# VUE POUR EXPORT PDF
# =============================================
@login_required
def export_report(request):
    """
    Génère le rapport PDF depuis le dashboard avec KPIs, graphiques, IA et narration
    """

    queryset = Transaction.objects.select_related("account").all()

    # 🔹 KPIs dynamiques
    total_transactions = queryset.count()
    total_income = float(queryset.filter(amount__gt=0).aggregate(Sum("amount"))["amount__sum"] or 0)
    total_expenses = float(queryset.filter(amount__lt=0).aggregate(Sum("amount"))["amount__sum"] or 0)
    net_balance = total_income + total_expenses

    # 🔹 Graphique exemple (répartition IN/OUT)
    labels = ["IN","OUT"]
    data = [
        float(queryset.filter(transaction_type="IN").aggregate(Sum("amount"))["amount__sum"] or 0),
        float(queryset.filter(transaction_type="OUT").aggregate(Sum("amount"))["amount__sum"] or 0)
    ]

    chart_buffer = io.BytesIO()
    plt.figure(figsize=(6,3))
    plt.bar(labels, data, color=["green","red"])
    plt.title("Répartition Crédit / Débit")
    plt.tight_layout()
    plt.savefig(chart_buffer, format='png')
    plt.close()
    chart_buffer.seek(0)

    # 🔹 Création PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_mensuel.pdf"'

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import A4

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Titre
    elements.append(Paragraph("RAPPORT MENSUEL FINANCIER - DASHBOARD", styles["Heading1"]))
    elements.append(Spacer(1,0.3*inch))
    elements.append(Paragraph(f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1,0.5*inch))

    # KPIs
    kpi_data = [
        ["Total Transactions", total_transactions],
        ["Total Revenus (XAF)", f"{total_income:,.0f}"],
        ["Total Dépenses (XAF)", f"{total_expenses:,.0f}"],
        ["Solde Net (XAF)", f"{net_balance:,.0f}"]
    ]
    table = Table(kpi_data, colWidths=[3*inch,2*inch])
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.grey)]))
    elements.append(table)
    elements.append(Spacer(1,0.5*inch))

    # Graphique
    elements.append(Image(chart_buffer, width=5*inch, height=3*inch))
    elements.append(Spacer(1,0.5*inch))

    # Analyse IA + Narration
    elements.append(Paragraph("Analyse IA", styles["Heading2"]))
    elements.append(Paragraph("Score de risque : 50/100", styles["Normal"]))
    elements.append(Paragraph("Synthèse narrative : Exemple de narration", styles["Normal"]))

    doc.build(elements)
    return response
from celery import shared_task
from .daily_kpis import compute_daily_kpis
from .alerts import cashflow_alert


@shared_task
def daily_finance_job():
    kpis = compute_daily_kpis()
    alert = cashflow_alert()
    return {
        "kpis": kpis,
        "alert": alert
    }

# finance/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import redirect
from .models import Document
from .forms import DocumentForm

from .models import Company, Account, Transaction, Invoice, Payment, Document
from .serializers import (
    CompanySerializer,
    AccountSerializer,
    TransactionSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    DocumentSerializer,
)



def dashboard(request):
    companies = Company.objects.count()
    accounts = Account.objects.count()
    invoices = Invoice.objects.count()
    transactions = Transaction.objects.count()

    return render(request, "finance/dashboard.html", {
        "companies": companies,
        "accounts": accounts,
        "invoices": invoices,
        "transactions": transactions,
    })


def account_list(request):
    accounts = Account.objects.all()
    return render(request, "finance/account_list.html", {"accounts": accounts})


def transaction_list(request):
    transactions = Transaction.objects.all().order_by("-date")
    return render(request, "finance/transaction_list.html", {"transactions": transactions})


def invoice_list(request):
    invoices = Invoice.objects.all().order_by("-created_at")
    return render(request, "finance/invoice_list.html", {"invoices": invoices})

def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("finance:documents-list")
    else:
        form = DocumentForm()

    return render(request, "finance/documents/upload.html", {"form": form})


def document_list(request):
    """
    Liste des documents financiers
    """
    documents = Document.objects.order_by("-uploaded_at")

    return render(
        request,
        "finance/document_list.html",
        {"documents": documents}
    )


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



# accounting/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from tasks.invoice_tasks import process_invoice_ocr



class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        Endpoint: POST /api/accounting/invoices/upload/
        Attends un fichier (raw_file) et crée l'Invoice, puis déclenche OCR en tâche asynchrone.
        """
        serializer = InvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        # set status ocr pending
        invoice.ocr_status = 'pending'
        invoice.save(update_fields=['ocr_status'])
        # trigger async OCR task
        try:
            process_invoice_ocr.delay(invoice.id)
        except Exception:
            # si Celery non configuré, on peut exécuter synchrone (fallback)
            try:
                process_invoice_ocr(invoice.id)
            except Exception as e:
                return Response({'detail': 'task_failed', 'error': str(e)}, status=500)
        return Response({'id': invoice.id, 'status': 'processing'}, status=202)


from django.shortcuts import render


def qr_scan(request):
    return render(request, 'sales_receipts/qr_scan.html')


def qr_upload(request):
    return render(request, 'sales_receipts/qr_scan.html')

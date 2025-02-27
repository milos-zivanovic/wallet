from django.shortcuts import render
from django.http import JsonResponse
from pyzbar.pyzbar import decode
from PIL import Image
import io


def qr_scan(request):
    return render(request, 'sales_receipts/qr_scan.html')


def qr_upload(request):
    print(request.method, request.FILES)

    if request.method != 'POST' or not request.FILES.get('image'):
        return JsonResponse({'result': 'Greška u upload-u.'}, status=404)

    image_data = request.FILES['image'].read()
    image = Image.open(io.BytesIO(image_data))
    qr_codes = decode(image)
    if qr_codes:
        result = qr_codes[0].data.decode('utf-8')
        return JsonResponse({'result': result}, status=200)
    else:
        return JsonResponse({'result': 'QR kod nije pronađen.'}, status=404)

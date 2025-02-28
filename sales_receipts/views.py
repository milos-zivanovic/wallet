import cv2
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage


def qr_scan(request):
    return render(request, 'sales_receipts/qr_scan.html')


def qr_upload(request):
    if request.method != 'POST' or not request.FILES.get('image'):
        return JsonResponse({'error': 'Greška u upload-u.'}, status=404)
    image_file = request.FILES['image']

    # Save the file temporarily to a known location
    file_path = default_storage.save('temp_image.jpg', image_file)
    image_path = default_storage.path(file_path)

    # Open image with OpenCV
    image = cv2.imread(image_path)

    # Initialize QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect and decode QR code using detectAndDecode method
    decoded_text, points, straight_qrcode = detector.detectAndDecode(image)

    if decoded_text:
        return JsonResponse({'result': decoded_text}, status=200)
    else:
        return JsonResponse({'error': 'Greška pri obradi slike.'}, status=404)

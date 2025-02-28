from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image


def qr_scan(request):
    return render(request, 'sales_receipts/qr_scan.html')


def qr_upload(request):
    if request.method != 'POST' or not request.FILES.get('image'):
        return JsonResponse({'result': 'Greška u upload-u.'}, status=404)
    image_file = request.FILES['image']

    try:
        image = Image.open(image_file)
        return JsonResponse({"result": 'Citanje QR koda u fazi implementacije.'}, status=200)

        # decoded_objects = decode(image)
        # if decoded_objects:
        #     qr_text = decoded_objects[0].data.decode("utf-8")
        #     return JsonResponse({"result": qr_text}, status=200)
        # else:
        #     return JsonResponse({"error": "QR kod nije pronađen na slici."}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"Greška pri obradi slike: {str(e)}"}, status=500)

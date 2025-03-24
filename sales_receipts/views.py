from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def qr_url_form(request):
    return render(request, 'sales_receipts/qr_url_form.html')


@csrf_exempt
def qr_url_upload(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Metoda nije dozvoljena.'}, status=405)

    qr_url = request.POST.get('qr_url')
    if not qr_url:
        return JsonResponse({'error': 'Url nije prosledjen ili nije validan.'}, status=400)

    return JsonResponse({'result': f'Uspesno obradjen url: {qr_url}'}, status=200)

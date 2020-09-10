from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.http import is_safe_url
import stripe

# Create your views here.
stripe.api_key = "sk_test_vAfJFRZxg6fkoVl9i8JuWLSB00EtyZSflC"
STRIPE_PUB_KEY = 'pk_test_ER5kn9tZut76yc1BJOuN3cYG00IByD0QYx'

def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_,request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY, "next_url": next_url})

def payment_method_createview(request):
    if request.method == "POST":
        print(request.POST)
        return JsonResponse({"message":"Success! Your card was added."})
    return HttpResponse("error",status_code=401)

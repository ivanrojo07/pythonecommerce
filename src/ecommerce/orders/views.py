from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
# Create your views here.
# from billing.models import BillingProfile
from .models import Order, ProductPurchase

class OrderListView(LoginRequiredMixin,ListView):
    def get_queryset(self):
        # my_profile = BillingProfile.objects.new_or_get(self.request)
        return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin,DetailView):
    
    def get_object(self):
        qs = Order.objects.by_request(
            self.request
        ).filter(
            order_id = self.kwargs.get('order_id')
        )
        if qs.count() == 1:
            return qs.first()
        raise Http404

class LibraryView(LoginRequiredMixin,ListView):
    template_name="orders/library.html"
    def get_queryset(self):
        return ProductPurchase.objects.product_by_request(self.request)
        # return ProductPurchase.objects.by_request(self.request).digital()

class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self.request.GET
            product_id = request.GET.get('product_id')
            if product_id is not None:
                product_id = int(product_id)
            ownership_ids = ProductPurchase.objects.product_by_id(request)
            if product_id in ownership_ids:
                return JsonResponse({'owner':True})
            return JsonResponse({'owner':False})
        raise Http404

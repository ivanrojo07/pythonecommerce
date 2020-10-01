# from django.views import ListView
from django.http import Http404, HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from .models import Product, ProductFile


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()

class UserProductHistoryView(LoginRequiredMixin,ListView):
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=True)#.all().filter(content_type__name="product")
        # viewed_ids = [x.object_id for x in views]
        return views


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)



class ProductListView(ListView):
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)



class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance



class ProductDetailView(ObjectViewedMixin, DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk, featured=True) #id
    # instance = get_object_or_404(Product, pk=pk, featured=True)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    #print(instance)
    # qs  = Product.objects.filter(id=pk)

    # #print(qs)
    # if qs.exists() and qs.count() == 1: # len(qs)
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)

from wsgiref.util import FileWrapper
from django.conf import settings
import os
from mimetypes import guess_type
from orders.models import ProductPurchase

class ProductDownloadView(View):
    def get(self, request,*args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk,product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        downloads_obj = downloads_qs.first()
        can_download = False
        user_ready = True
        if downloads_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False
        purchased_products = Product.objects.none()
        if downloads_obj.free:
            can_download = True
            user_ready = True
        else:
            purchased_products = ProductPurchase.objects.product_by_request(request)
            if downloads_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to this item")
            return redirect(downloads_obj.get_default_url())


        # if  downloads_obj.free:
        #     can_download = True

        # else:
        #     purchased_products = ProductPurchase.object.product_by_request(request)
        #     if downloads_obj.product in purchased_products:
        #         can_download=True

        # if downloads_obj.user_required:
        #     if request.user.is_authenticated:
        #         can_download = True
        #     else:
        #         can_download = False

        file_root = settings.PROTECTED_ROOT
        filepath = downloads_obj.file.path
        final_filepath = os.path.join(file_root,filepath)
        with open(final_filepath,'rb') as f:
            wraper = FileWrapper(f)
            mimetype = "application/force-download"
            gussed_mimetype = guess_type(filepath)[0]
            if gussed_mimetype:
                mimetype = gussed_mimetype
            response = HttpResponse(wraper, content_type = mimetype)
            response['Content-Disposition'] = "attachment;filename=%s" %(downloads_obj.name)
            response["X-SendFile"] = str(downloads_obj.name)
            return response
        return redirect(downloads_obj.get_default_url())

        # qs = Product.objects.filter(slug=slug)
        # if qs.count() != 1:
        #     raise Http404("Product not found")
        # product_obj = qs.first()
        # downloads_qs = product_obj.get_downloads().filter(pk=pk)
        # if downloads_qs.count() != 1:
        #     raise Http404("Download not found")
        # downloads_obj = downloads_qs.first()

        # response = HttpResponse(downloads_obj.get_download_url())
        # return response
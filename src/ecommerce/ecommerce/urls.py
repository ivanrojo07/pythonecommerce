"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from accounts.views import login_page, register_page, guest_register_view

from addresses.views import checkout_address_create_view, checkout_address_reuse_view

from carts.views import cart_detail_api_view

from .views import home_page,about_page,contact_page#,login_page,register_page
from django.views.generic import TemplateView

from carts.views import cart_home
# from products.views import (
#                     ProductListView, 
#                     product_list_view, 
#                     ProductDetailView, 
#                     product_detail_view,
#                     ProductFeaturedListView,
#                     ProductFeaturedDetailView,
#                     ProductDetailSlugView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page, name="home"),
    path('about/',about_page,name="about"),
    path('contact/',contact_page, name="contact"),
    path('login/',login_page, name="login"),
    path('register/guest',guest_register_view, name="guest_register"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('register/',register_page, name="register"),

    path('api/cart/', cart_detail_api_view, name="api-cart"),

    path('checkout/address/create/', checkout_address_create_view, name="checkout_address_create"),
    path('checkout/address/reuse/', checkout_address_reuse_view, name="checkout_address_reuse"),

    # path('cart/',cart_home, name="cart"),
    path('cart/', include('carts.urls', namespace='cart')),
    path('bootstrap/',TemplateView.as_view(template_name='bootstrap/example.html')),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    # path('products/', ProductListView.as_view()),
    # path('products-fbv/', product_list_view),
    # # path('products/<int:pk>/', ProductDetailView.as_view()),
    # path('products-fbv/<int:pk>/', product_detail_view),
    # path('featured/',ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/',ProductFeaturedDetailView.as_view()),
    # path('products/<slug:slug>/',ProductDetailSlugView.as_view())
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

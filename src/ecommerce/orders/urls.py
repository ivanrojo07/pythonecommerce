
from django.urls import path, re_path

from .views import (
                    OrderDetailView, 
                    OrderListView)

app_name = "orders"
urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    re_path('detail/(?P<order_id>[0-9A-Za-z]+)/$',OrderDetailView.as_view(), name='detail')
]
